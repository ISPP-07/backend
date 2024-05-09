import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from src.core.config import settings
from src.modules.shared.auth.model import RefreshToken
from src.modules.shared.user import model
from src.core.utils.security import get_hashed_password

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
        await create_superuser(_client_db)
        await create_ttl_index(_client_db, RefreshToken, "expires_at", 0)
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


async def create_superuser(client: AsyncIOMotorClient) -> None:
    db = client.get_database(settings.MONGO_DB)
    superuser = await model.User.get(db, {'username': settings.FIRST_SUPERUSER_USERNAME})
    if superuser is None:
        first_superuser = {
            'master': True,
            'username': settings.FIRST_SUPERUSER_USERNAME,
            'password': get_hashed_password(settings.FIRST_SUPERUSER_PASSWORD),
            'email': settings.FIRST_SUPERUSER_EMAIL
        }
        await model.User.create(db, first_superuser)


async def create_ttl_index(client: AsyncIOMotorClient, collection: model, field_name: str, expire_after_seconds: int):
    db = client.get_database(settings.MONGO_DB)
    collection: AsyncIOMotorCollection = db[collection._get_collection_name()]
    await collection.create_index([(field_name, 1)], expireAfterSeconds=expire_after_seconds)
