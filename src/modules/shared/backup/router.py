from fastapi import APIRouter, File, UploadFile, status

from src.core.deps import DataBaseDep
from src.modules.shared.backup import controller


router = APIRouter(tags=['Backup'])


@router.get('/dump', status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {'description': 'Successful Response'},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        'description': 'Internal Server Error'}
})
async def generate_backup(db: DataBaseDep, password: str):
    """
    Generates a backup of the database.
    """
    return await controller.generate_backup_controller(db, password)


@router.post('/restore', status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {'description': 'Successful Response'},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        'description': 'Internal Server Error'}
})
async def restore_backup(db: DataBaseDep, password: str, file: UploadFile = File(...)):
    """
    Restores a backup of the database.
    """
    return await controller.restore_backup_controller(db, password, file)
