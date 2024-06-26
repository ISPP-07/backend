import datetime
import uuid
import json
from typing import Dict, List, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings


class BackupEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


def convert_ids_to_uuid(document: Dict[str, Any]) -> None:
    for key, value in document.items():
        if isinstance(value, dict):
            convert_ids_to_uuid(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    convert_ids_to_uuid(item)
        elif key.endswith('id') or key.endswith('_id'):
            try:
                document[key] = uuid.UUID(value)
            except (TypeError, ValueError):
                pass


async def get_database_session() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(
        str(settings.MONGO_DATABASE_URI),
        uuidRepresentation='standard',
    )
    db = client.get_database(settings.MONGO_DB)
    return db


async def populate_from_json(db: AsyncIOMotorDatabase, data: Dict[str, List[Dict[str, Any]]]) -> None:
    for collection, collection_data in data.items():
        await db[collection].delete_many({})
        if collection_data:
            for document in collection_data:
                convert_ids_to_uuid(document)
            await db[collection].insert_many(collection_data)


async def dump_to_json(db: AsyncIOMotorDatabase) -> Dict[str, Any]:
    json_data = {}
    collections = await db.list_collection_names()
    for collection in collections:
        documents = await db[collection].find().to_list(None)
        json_data[collection] = documents
    return json_data
