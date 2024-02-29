from typing import Any

from fastapi import APIRouter, status

from src.core.deps import SessionDep
from src.modules.acat.appointment.controller import create_appointment_controller
from src.modules.acat.appointment.model import Appointment

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_appointment(session: SessionDep, appointment: Appointment)->Any:
    return await create_appointment_controller(session, appointment)

