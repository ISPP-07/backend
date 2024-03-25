from pydantic import UUID4, ValidationError
import os

from fastapi import HTTPException, status, UploadFile
import openpyxl

from src.core.utils.helpers import parse_validation_error, generate_alias
from src.core.deps import DataBaseDep
from src.modules.acat.patient import model
from src.modules.acat.patient import service


async def get_patients_controller(db: DataBaseDep):
    return await service.get_patients_service(db)


async def create_patient_controller(db: DataBaseDep, patient: model.PatientCreate) -> model.Patient:
    check_patient = await service.get_patient_service(db, query={'nid': patient.nid})
    if check_patient is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'There is already one patient with nid {patient.nid}'
        )
    if patient.alias is None:
        patient.alias = generate_alias(
            patient.name, patient.first_surname, patient.second_surname
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
                alias=generate_alias(row[0], row[1], row[2]),
                nid=row[3],
                birth_date=row[4],
                gender='Man' if row[5] == 'Hombre' else 'Woman',
                address=row[6],
                contact_phone=str(row[7]),
                dossier_number=row[8],
                first_technician=row[9],
                observation=row[10],
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


async def update_patient_controller(
    db: DataBaseDep,
    patient_id: UUID4,
    patient: model.PatientUpdate
) -> model.Patient:
    patient_db = await service.get_patient_service(db, query={'id': patient_id})
    if patient_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Patient not found',
        )
    if patient.nid is not None:
        check_nid = await service.get_patient_service(db, query={'nid': patient.nid})
        if check_nid is not None and check_nid.id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'There is already a patient with nid {patient.nid}',
            )
    request_none_fields = [
        field for field in model.PATIENT_NONE_FIELDS
        if field in patient.update_fields_to_none
    ]
    update_data = patient.model_dump(exclude='update_fields_to_none')
    patient.first_surname
    patient.second_surname
    patient.name
    for field in update_data.copy():
        if field in request_none_fields:
            continue
        if update_data[field] is None:
            update_data.pop(field)
    updated_patient = await service.update_patient_service(db, patient_id, update_data)
    return updated_patient


async def delete_patient_controller(db: DataBaseDep, patient_id: UUID4):
    await service.delete_patient_service(db, query={'id': patient_id})
