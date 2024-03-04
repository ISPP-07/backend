from fastapi import APIRouter, status, HTTPException

from src.core.deps import SessionDep
from src.modules.shared.user.schema import UserOut
from src.modules.shared.user.controller import create_user_controller
from src.modules.shared.user.schema import UserCreate

router = APIRouter()


@router.get('/')
def root():
    return 'Hello shared user router!'


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(session: SessionDep, user_in: UserCreate) -> UserOut:
    user = await create_user_controller(session, user_in)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )

    return user
