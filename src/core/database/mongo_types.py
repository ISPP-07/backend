from typing import Any


class DeleteResultMongo():
    acknowledged: bool
    deleted_count: int


class InsertOneResultMongo():
    acknowledged: bool
    inserted_id: Any


class InsertResultMongo():
    acknowledged: bool
    inserted_ids: list[Any]


class UpdateResult():
    matched_count: int
    modified_count: int
    upserted_id: Any | None
