from fastapi import APIRouter, status, Request, HTTPException

from src.core.deps import DataBaseDep
from src.modules.shared.user.model import UserCreate, UserOut
from src.modules.shared.user.controller import create_user_controller

router = APIRouter()


@router.get('/')
def root():
    return 'Hello shared user router!'


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(db: DataBaseDep, request: Request, user: UserCreate):
    session = request.state.mongo_session
    result = await create_user_controller(db, session, user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )
    return result
