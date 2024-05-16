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