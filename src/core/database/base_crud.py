import copy
from typing import TypeVar, Type, Any
from uuid import uuid4
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.core.database.mongo_types import DeleteResultMongo, InsertOneResultMongo
from src.core.utils.helpers import check_all_keys, change_invalid_types_mongo

Self = TypeVar('Self', bound='BaseMongo')


class BaseMongo(BaseModel):

    @classmethod
    def _get_collection_name(cls):
        return cls.__name__

    @staticmethod
    def prepare_query(query: dict):
        if check_all_keys(query, 'id'):
            query['_id'] = query.pop('id')
        return query

    @classmethod
    async def get(
        cls: Type[Self],
        db: AsyncIOMotorDatabase,
        query: dict,
        **kwargs: Any,
    ) -> Self | None:
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        result = await collection.find_one(cls.prepare_query(query), **kwargs)
        return cls.from_mongo(result)

    @classmethod
    async def get_multi(
        cls: Type[Self],
        db: AsyncIOMotorDatabase,
        query: dict | None,
        **kwargs: Any,
    ) -> list[Self]:
        if query is None:
            query = {}
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        cursor = collection.find(cls.prepare_query(query), **kwargs)
        result = await cursor.to_list(length=None)
        return [cls.from_mongo(document) for document in result]

    @classmethod
    async def create(
        cls: Type[Self],
        db: AsyncIOMotorDatabase,
        obj_to_create: dict,
        **kwargs: Any,
    ) -> InsertOneResultMongo:
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        if 'id' in obj_to_create:
            obj_to_create.pop('id')
        if '_id' in obj_to_create:
            obj_to_create.pop('_id')
        obj = cls(**obj_to_create, id=uuid4())
        return await collection.insert_one(obj.mongo(), **kwargs)

    @classmethod
    async def update(
        cls: Type[Self],
        db: AsyncIOMotorDatabase,
        query: dict,
        data_to_update: dict,
        **kwargs: Any,
    ) -> Self | None:
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        if 'id' in data_to_update:
            data_to_update.pop('id')
        if '_id' in data_to_update:
            data_to_update.pop('_id')
        for key, value in copy.deepcopy(data_to_update).items():
            if value is None:
                data_to_update.pop(key)
        change_invalid_types_mongo(data_to_update)
        update = {'$set': data_to_update}
        result = await collection.find_one_and_update(
            cls.prepare_query(query),
            update,
            return_document=True,
            **kwargs
        )
        return cls.from_mongo(result)

    @classmethod
    async def delete(
        cls: Type[Self],
        db: AsyncIOMotorDatabase,
        query: dict,
        many: bool = False,
        **kwargs: Any,
    ) -> DeleteResultMongo:
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        if many:
            result = await collection.delete_many(cls.prepare_query(query), **kwargs)
        else:
            result = await collection.delete_one(cls.prepare_query(query), **kwargs)
        return result

    @classmethod
    async def count(
        cls: Type[Self],
        db: AsyncIOMotorDatabase,
        query: dict,
        **kwargs: Any,
    ):
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        result = await collection.count_documents(cls.prepare_query(query), **kwargs)
        return result

    @classmethod
    def get_collection(
            cls: Type[Self],
            db: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
        return db[cls._get_collection_name()]

    @classmethod
    def from_mongo(cls: Type[Self], data: dict | None):
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)
        parsed = self.model_dump(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )
        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')
        change_invalid_types_mongo(parsed)
        return parsed
