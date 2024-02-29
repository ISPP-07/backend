from src.modules.acat.appointment.model import Appointment

from src.modules.acat.appointment.service import create_appointment_service


async def create_appointment_controller(session, appointment: Appointment):
    return await create_appointment_service(session, appointment)

