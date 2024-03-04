from src.modules.acat.appointment.model import Appointment
from src.modules.acat.patient.model import Technician, Patient


async def get_technician_by_id(session, technician_id: int):
    return await Technician.get(session, id=technician_id)


async def update_technician_appointments(session, technician: Technician, appointment: Appointment):
    if technician.appointments is None:
        technician.appointments = []
    technician.appointments.append(appointment)
    await Technician.update(session, technician=technician)
    return technician.model_dump()


async def get_patient_by_id(session, patient_id: int):
    return await Patient.get(session, id=patient_id)


async def update_patient_appointments(session, patient: Patient, appointment: Appointment):
    if patient.appointments is None:
        patient.appointments = []
    patient.appointments.append(appointment)
    await Patient.update(session, patient=patient)
    return patient


async def create_appointment(session, appointment_data):
    appointment = await Appointment.create(session, **appointment_data.model_dump())
    return appointment
