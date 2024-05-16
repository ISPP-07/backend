import pytest
from fastapi import status, HTTPException
from unittest.mock import AsyncMock
from src.core.deps import DataBaseDep
from src.modules.shared.backup import service
from src.modules.shared.backup.controller import generate_backup_controller, restore_backup_controller

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.fixture
def mock_file():
    return AsyncMock()

@pytest.mark.asyncio
async def test_generate_backup_controller_success(mock_db, mock_file):
    # Mock the generate_backup_service function
    service.generate_backup_service = AsyncMock(return_value="backup_generated")

    result = await generate_backup_controller(mock_db, "password")

    assert result == "backup_generated"
    service.generate_backup_service.assert_called_once_with(mock_db, "password")

@pytest.mark.asyncio
async def test_generate_backup_controller_error(mock_db, mock_file):
    # Mock the generate_backup_service function to raise an exception
    service.generate_backup_service = AsyncMock(side_effect=Exception("Something went wrong"))

    with pytest.raises(HTTPException) as exc_info:
        await generate_backup_controller(mock_db, "password")

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert str(exc_info.value.detail) == "Internal Server Error Something went wrong"
    service.generate_backup_service.assert_called_once_with(mock_db, "password")

@pytest.mark.asyncio
async def test_restore_backup_controller_success(mock_db, mock_file):
    # Mock the restore_backup_service function
    service.restore_backup_service = AsyncMock(return_value="backup_restored")

    result = await restore_backup_controller(mock_db, "password", mock_file)

    assert result == "backup_restored"
    service.restore_backup_service.assert_called_once_with(mock_db, "password", mock_file)
