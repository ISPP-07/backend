
from sqlmodel import select, func
from sqlalchemy.orm import aliased, joinedload

from src.modules.acat.patient.model import Patient, PatientObservation
from src.modules.acat.appointment.model import Appointment
from src.modules.acat.patient.model import Technician


async def get_patient_details_service(session, patient_id: int):
    appointment_subq = (
        select(
            Appointment.patient_id,
            Appointment.technician_id,
            func.row_number().over(
                partition_by=Appointment.patient_id,
                order_by=Appointment.appointment_date.asc()
            ).label("rn")
        )
        .filter(Appointment.patient_id == patient_id)
        .subquery()
    )

    first_technician = aliased(Technician)

    # Modificar la consulta para seleccionar también los detalles del Technician y la observación del paciente
    patient_query = (
        select(
            Patient,
            first_technician.name.label("technician_name"),
            PatientObservation.observation_text  # Selecciona el texto de la observación
        )
        .join(appointment_subq, Patient.id == appointment_subq.c.patient_id)
        .join(first_technician, first_technician.id == appointment_subq.c.technician_id)
        # Une la tabla de observaciones
        .join(PatientObservation, PatientObservation.patient_id == Patient.id)
        # Considera solo el primer nombramiento
        .where(appointment_subq.c.rn == 1)
        .options(joinedload(Patient.observations))  # Eager load observations
        .filter(Patient.id == patient_id)
    )

    result = await session.execute(patient_query)
    # Incluye observation_text en la desestructuración
    patient, technician_name, observation_text = result.first()
    result = patient.model_dump()
    result["first_technician_name"] = technician_name
    # Añade observation_text al resultado
    result["observation_text"] = observation_text

    return result
