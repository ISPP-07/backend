import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings

if 'win' in sys.platform:
    # Set event loop policy for Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

_client_db: AsyncIOMotorClient = None  # pylint: disable=C0103


async def connect_and_init_db():
    global _client_db  # pylint: disable=W0603
    try:
        _client_db = AsyncIOMotorClient(
            str(settings.MONGO_DATABASE_URI),
            uuidRepresentation='standard',
        )
    except Exception as e:
        raise e


async def close_db_connection():
    global _client_db  # pylint: disable=W0603
    if _client_db is None:
        return
    _client_db.close()
    _client_db = None


def get_client() -> AsyncIOMotorClient:
    return _client_db
