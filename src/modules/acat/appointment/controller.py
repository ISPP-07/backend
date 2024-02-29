from src.modules.acat.appointment.service import get_appointment_list_details_service


async def get_appointment_list_details_controller(session):
    return await get_appointment_list_details_service(session)
