from typing import List
from fastapi import APIRouter, status

from src.core.deps import SessionDep
from src.modules.acat.appointment.controller import get_appointment_list_details_controller
from src.modules.acat.appointment.model import Appointment

router = APIRouter()


@router.get('/list', status_code=status.HTTP_200_OK)
async def get_appointment_list_details(session: SessionDep) -> List[Appointment]:
    return await get_appointment_list_details_controller(session)
