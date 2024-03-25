from pydantic import UUID4, ValidationError
import os

from fastapi import HTTPException, status, UploadFile
import openpyxl

from src.core.utils.helpers import parse_validation_error
from src.modules.acat.patient import service
from src.modules.acat.patient import model
from src.core.deps import DataBaseDep


async def get_patients_controller(db: DataBaseDep):
    return await service.get_patients_service(db)


async def create_patient_controller(db: DataBaseDep, patient: model.PatientCreate) -> model.Patient:
    check_patient = await service.get_patient_service(db, query={'nid': patient.nid})
    if check_patient is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'There is already one patient with nid {patient.nid}'
        )
    mongo_insert = await service.create_patient_service(db, patient)
    result = await service.get_patient_service(db, query={'id': mongo_insert.inserted_id})
    return result


async def get_patient_details_controller(db: DataBaseDep, patient_id: UUID4):
    result = await service.get_patient_service(db, query={'id': patient_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found',
        )
    return result


async def upload_excel_patients_controller(db: DataBaseDep, patients: UploadFile) -> None:
    [_, extension] = os.path.splitext(patients.filename)
    if extension[1:] not in ['xlsx', 'xlsm']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                'The files with extension ',
                f'"{extension[1:]}" are not supported.'
            )
        )
    fields_excel = [
        'nombre',
        'primer apellido',
        'segundo apellido',
        'dni',
        'fecha nacimiento',
        'genero',
        'direccion',
        'telefono',
        'numero expediente',
        'tecnico',
        'observacion']
    wb = openpyxl.load_workbook(patients.file)
    ws = wb.active
    first_row = [
        ws.cell(row=1, column=i).value
        for i in range(1, len(fields_excel) + 1)
    ]
    if len(first_row) != len(fields_excel) and not all(
            field in fields_excel for field in first_row):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The excel file is incorrect'
        )
    patients_excel: list[model.PatientCreate] = []
    for row in ws.iter_rows(
            min_row=2,
            min_col=1,
            max_col=11,
            values_only=True):
        if all(value is None for value in row):
            continue
        if row[0] is None or row[1] is None or row[3] is None or row[4] is None or row[8] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The excel file is incorrect'
            )
        if row[5] not in ['Hombre', 'Mujer']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The excel file is incorrect'
            )
        try:
            new_patient = model.PatientCreate(
                name=row[0],
                first_surname=row[1],
                second_surname=row[2],
                nid=row[3],
                birth_date=row[4],
                gender='Man' if row[5] == 'Hombre' else 'Woman',
                address=row[6],
                contact_phone=str(row[7]),
                dossier_number=row[8],
                first_technician=row[9],
                observations=row[10],
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=parse_validation_error(e.errors())
            )
        patients_excel.append(new_patient)
        patients_db = await service.get_patients_service(db, query={'nid': {'$in': [p.nid for p in patients_excel]}})
        for patient in patients_excel:
            patient_db: model.Patient | None = next(
                (p for p in patients_db if p.nid == patient.nid), None
            )
            if patient_db is None:
                await service.create_patient_service(db, patient)
            else:
                update_patient = model.PatientUpdate(**patient.model_dump())
                await service.update_one_patient_service(
                    db,
                    query={'nid': patient.nid},
                    update=update_patient,
                    upsert=True,
                )
