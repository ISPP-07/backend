from typing import Optional
from datetime import date

from fastapi import APIRouter, status, UploadFile
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.server import dependencies
from src.modules.acat.patient import controller
from src.modules.acat.patient import model

router = APIRouter(tags=['Patient'], dependencies=dependencies)


@router.get('',
            status_code=status.HTTP_200_OK,
            response_model=model.GetPatients,
            responses={
                200: {"description": "Successful Response"},
                500: {"description": "Internal Server Error"}
            })
async def get_patients(
    db: DataBaseDep,
    alias: Optional[str] = None,
    name: Optional[str] = None,
    nid: Optional[str] = None,
    is_rehabilitated: Optional[bool] = None,
    before_registration_date: Optional[date] = None,
    after_registration_date: Optional[date] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    **Retrieve a list of all patients.**

    Queries the database and returns a list of all patients. Each patient includes their ID,
    name, first surname, second surname (if any), automatically generated alias, national
    identification number (nid), birth date, gender (if any), address (if any), contact phone (if any),
    dossier number, first technician assigned to the patient (if any), registration date, any
    observations about the patient, and the calculated age of the patient.
    """
    return await controller.get_patients_controller(
        db,
        alias, name, nid, is_rehabilitated,
        before_registration_date, after_registration_date,
        limit, offset
    )


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=model.Patient,
             responses={
                 201: {"description": "Patient created successfully"},
                 400: {"description": "Bad Request - Invalid data input"},
                 500: {"description": "Internal Server Error"}
             })
async def create_patient(db: DataBaseDep, patient: model.PatientCreate):
    """
    **Create a new patient.**

    Accepts patient information and creates a new patient record in the database. Required
    information includes the patient's name, first surname, national identification number (nid),
    birth date, dossier number, and optional fields such as second surname, gender, address,
    contact phone, first technician, and any observations.
    """
    return await controller.create_patient_controller(db, patient)


@router.patch(
    '/{patient_id}',
    status_code=status.HTTP_200_OK,
    response_model=model.Patient,
    responses={
        200: {"description": "Patient updated successfully"},
        400: {"description": "NID is duplicated"},
        404: {"description": "Patient not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def update_patient(db: DataBaseDep, patient_id: UUID4, patient: model.PatientUpdate):
    """
    **Update a patient.**

    Accepts patient information and update his information in the database.

    """
    return await controller.update_patient_controller(db, patient_id, patient)


@router.get('/{patient_id}',
            status_code=status.HTTP_200_OK,
            response_model=model.PatientOut,
            responses={
                200: {"description": "Successful Response"},
                404: {"description": "Patient not found"},
                500: {"description": "Internal Server Error"}
            })
async def get_patient_details(db: DataBaseDep, patient_id: UUID4):
    """
    **Get detailed information about a specific patient.**

    Fetches and returns detailed information about a specific patient identified by their UUID.
    This includes all the fields available in the PatientOut model: ID, name, first surname,
    second surname (if any), alias, national identification number (nid), birth date, gender (if any),
    address (if any), contact phone (if any), dossier number, registration date, first technician
    (if any), any observations, and the patient's calculated age.
    """
    return await controller.get_patient_details_controller(db, patient_id)


@router.post(
    '/excel',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        200: {"description": "Patients in excel created successfully"},
        400: {"description": "The data was incorrect"},
    }
)
async def upload_excel_patient(db: DataBaseDep, patients: UploadFile):
    return await controller.upload_excel_patients_controller(db, patients)


@router.delete(
    '/{patient_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Patient deleted successfully"},
        404: {"description": "Patient not found"},
        500: {"description": "Patient Server Error"}
    }
)
async def delete_patient(db: DataBaseDep, patient_id: UUID4):
    """
    **Delete a patient.**
    Deletes a patient record from the database based on the patient's UUID.
    """
    return await controller.delete_patient_controller(db, patient_id)
