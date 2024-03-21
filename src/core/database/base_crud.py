import copy
from typing import Any, Self
from uuid import uuid4
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.core.database.mongo_types import (
    DeleteResultMongo,
    InsertOneResultMongo,
    UpdateResult,
    InsertResultMongo,
)
from src.core.utils.helpers import check_all_keys, change_invalid_types_mongo


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
        cls: Self,
        db: AsyncIOMotorDatabase,
        query: dict,
        **kwargs: Any,
    ) -> Self | None:
        """
        Retrieves a single document from the database based on the provided query.

        This method is a class method that allows fetching a single document from the MongoDB
        collection associated with the class. It executes a find_one operation on the collection
        with the provided query and additional keyword arguments.

        Parameters:
        - db (AsyncIOMotorDatabase): The database instance to perform the operation on.
        - query (dict): The query criteria to search for a document.
        - **kwargs (Any): Additional keyword arguments to be passed to the find_one operation.

        Returns:
        - Self | None: An instance of the class representing the retrieved document, or None if not found.
        """
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        result = await collection.find_one(cls.prepare_query(query), **kwargs)
        return cls.from_mongo(result)

    @classmethod
    async def get_multi(
        cls: Self,
        db: AsyncIOMotorDatabase,
        query: dict | None = None,
        **kwargs: Any,
    ) -> list[Self]:
        """
        Retrieves a multiple documents from the database based on the provided query.

        This method is a class method that allows fetching multiple documents from a MongoDB collection
        using a specified query. It returns a list of instances of the class.

        Parameters:
        - db (AsyncIOMotorDatabase): The MongoDB database to query.
        - query (dict, optional): The query to filter the documents. Defaults to None.
        - **kwargs (Any): Additional keyword arguments that can be passed to the MongoDB query.

        Returns:
        list[Self]: A list of instances of the class representing the retrieved documents.

        Note:
        - If no query is provided, an empty query is used to retrieve all documents.
        """
        if query is None:
            query = {}
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        cursor = collection.find(cls.prepare_query(query), **kwargs)
        result = await cursor.to_list(length=None)
        return [cls.from_mongo(document) for document in result]

    @classmethod
    async def create(
        cls: Self,
        db: AsyncIOMotorDatabase,
        obj_to_create: dict,
        **kwargs: Any,
    ) -> InsertOneResultMongo:
        """
        Asynchronously creates a new document in the specified MongoDB database.

        This method creates a new document in the MongoDB collection associated with the class.
        It generates a unique identifier for the document and inserts it into the collection.

        Parameters:
        - db (AsyncIOMotorDatabase): The MongoDB database to operate on.
        - obj_to_create (dict): The dictionary containing the data for the new document.
        - **kwargs (Any): Additional keyword arguments to be passed to the insert operation.

        Returns:
        InsertOneResultMongo: An object representing the result of the insert operation.
        """
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        if 'id' in obj_to_create:
            obj_to_create.pop('id')
        if '_id' in obj_to_create:
            obj_to_create.pop('_id')
        obj: Self = cls(**obj_to_create, id=uuid4())
        return await collection.insert_one(obj.mongo(), **kwargs)

    @classmethod
    async def create_many(
        cls: Self,
        db: AsyncIOMotorDatabase,
        objs_to_create: list[dict],
        **kwargs: Any,
    ) -> InsertResultMongo:
        """
        Asynchronously creates a new documents in the specified MongoDB database.

        This method creates new documents in the MongoDB collection associated with the class.
        It generates a unique identifier for the documents and inserts it into the collection.

        Parameters:
        - db (AsyncIOMotorDatabase): The MongoDB database to operate on.
        - objs_to_create (list): The list containing the data for the new documents.
        - **kwargs (Any): Additional keyword arguments to be passed to the insert operation.

        Returns:
        InsertOneResultMongo: An object representing the result of the insert operation.
        """
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        objs_insert = []
        for obj in objs_to_create:
            if 'id' in obj:
                obj.pop('id')
            if '_id' in obj:
                obj.pop('_id')
            obj = cls(**obj, id=uuid4())
            objs_insert.append(obj.mongo())
        return await collection.insert_many(objs_insert, **kwargs)

    @classmethod
    async def update(
        cls: Self,
        db: AsyncIOMotorDatabase,
        query: dict,
        data_to_update: dict,
        **kwargs: Any,
    ) -> Self | None:
        """
        Asynchronously updates a document in the specified MongoDB database based on the provided query.

        Parameters:
        - db (AsyncIOMotorDatabase): The database to perform the update operation on.
        - query (dict): A dictionary representing the query to find the document to update.
        - data_to_update (dict): A dictionary containing the data to update in the document.
        - **kwargs (Any): Additional keyword arguments that can be passed to the update operation.

        Returns:
        Self | None: An instance of the class with the updated data if successful, None otherwise.
        """
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
    async def update_many(
        cls: Self,
        db: AsyncIOMotorDatabase,
        query: dict,
        data_to_update: dict,
        **kwargs: Any,
    ) -> UpdateResult:
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
        result = await collection.update_many(
            cls.prepare_query(query),
            update,
            **kwargs
        )
        return result

    @classmethod
    async def delete(
        cls: Self,
        db: AsyncIOMotorDatabase,
        query: dict,
        many: bool = False,
        **kwargs: Any,
    ) -> DeleteResultMongo:
        """
        A class method to delete documents from a MongoDB database based on a query.

        This method allows for the deletion of one or multiple documents from a MongoDB collection
        based on the provided query. It can delete either a single document or multiple documents
        depending on the 'many' parameter.

        Parameters:
        - db (AsyncIOMotorDatabase): The MongoDB database to perform the deletion operation on.
        - query (dict): The query to filter the documents to be deleted.
        - many (bool): A flag indicating whether to delete multiple documents (default is False).
        - **kwargs (Any): Additional keyword arguments to be passed to the delete operation.

        Returns:
        DeleteResultMongo: An object representing the result of the delete operation.
        """
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        if many:
            result = await collection.delete_many(cls.prepare_query(query), **kwargs)
        else:
            result = await collection.delete_one(cls.prepare_query(query), **kwargs)
        return result

    @classmethod
    async def count(
        cls: Self,
        db: AsyncIOMotorDatabase,
        query: dict,
        **kwargs: Any,
    ):
        collection: AsyncIOMotorCollection = db[cls._get_collection_name()]
        result = await collection.count_documents(cls.prepare_query(query), **kwargs)
        return result

    @classmethod
    def get_collection(
            cls: Self,
            db: AsyncIOMotorDatabase
    ) -> AsyncIOMotorCollection:
        return db[cls._get_collection_name()]

    @classmethod
    def from_mongo(cls: Self, data: dict | None):
        if not data:
            return data
        data_id = data.pop('_id', None)
        return cls(**dict(data, id=data_id))

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
