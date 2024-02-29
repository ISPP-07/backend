
from src.modules.acat.appointment.model import Appointment


async def get_appointment_list_details_service(session):
    '''
    Obtiene la lista de citas con los detalles de los pacientes y los técnicos

    Args:session: SessionDep
    Returns: List[Appointment]
    '''

    return await Appointment.get_multi(session, load_strategy={Appointment.technician: "selectin",
                                                               Appointment.patient: "selectin"})


# El codigo de abajo intenta traer los objetos en vez de los ids usando sqlalchemy
# async def get_appointment_list_details_service(session: Session):
#     result = await session.execute(
#         select(Appointment).options(
#             selectinload(Appointment.technician),
#             selectinload(Appointment.patient)
#         )
#     )
#     appointments = result.scalars().all()
#     return appointments
