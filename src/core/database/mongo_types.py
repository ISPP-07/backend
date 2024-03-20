from typing import Any


class DeleteResultMongo():
    acknowledged: bool
    deleted_count: int


class InsertOneResultMongo():
    acknowledged: bool
    inserted_id: Any


class UpdateResult():
    matchedCount: int
    modifiedCount: int
    upsertedId: Any | None
