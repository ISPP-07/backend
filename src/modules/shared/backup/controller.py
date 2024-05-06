from fastapi import status, HTTPException

from src.core.deps import DataBaseDep
from src.modules.shared.backup import service


async def generate_backup_controller(db: DataBaseDep, password: str):
    try:
        return await service.generate_backup_service(db, password)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        ) from e


async def restore_backup_controller(db: DataBaseDep, password: str, file):
    try:
        return await service.restore_backup_service(db, password, file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error {e}"
        ) from e
