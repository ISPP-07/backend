from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends

from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.database.session import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]
