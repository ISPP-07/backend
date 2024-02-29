from src.modules.acat.appointment.model import Appointment
from src.modules.acat.patient.model import Technician, Patient


async def get_technician_by_id(session, technician_id: int):
    return await Technician.get(session, id=technician_id)


async def update_technician_appointments(session, technician: Technician, appointment: Appointment):
    technician.appointments.append(appointment)
    await Technician.update(session, technician=technician)


async def get_patient_by_id(session, patient_id: int):
    return await Patient.get(session, id=patient_id)


async def update_patient_appointments(session, patient: Patient, appointment: Appointment):
    patient.appointments.append(appointment)
    await Patient.update(session, patient=patient)


async def create_appointment_service(session, appointment: Appointment):
    technician = await get_technician_by_id(session, appointment.technician_id)
    await update_technician_appointments(session, technician, appointment)
    patient = await get_patient_by_id(session, appointment.patient_id)
    await update_patient_appointments(session, patient, appointment)
    obj = await Appointment.create(session, **appointment.model_dump())

    return obj.model_dump()
