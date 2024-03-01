from fastapi import HTTPException

from src.modules.acat.appointment.model import Appointment
from src.modules.acat.appointment.service import (
    get_technician_by_id,
    get_patient_by_id,
    update_technician_appointments,
    update_patient_appointments,
    create_appointment
)


async def create_appointment_controller(session, appointment: Appointment):
    technician = await get_technician_by_id(session, appointment.technician_id)
    patient = await get_patient_by_id(session, appointment.patient_id)

    if technician is None or patient is None:
        raise HTTPException(status_code=404, detail="Item not found")

    appointment = await create_appointment(session, appointment)

    update_technician_appointments(session, technician, appointment)
    update_patient_appointments(session, patient, appointment)

    return appointment.model_dump()
