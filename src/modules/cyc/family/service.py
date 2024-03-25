from fastapi import HTTPException, status

from pydantic import UUID4
from src.core.deps import DataBaseDep
from src.core.database.mongo_types import InsertOneResultMongo, DeleteResultMongo
from src.modules.cyc.family import model


async def get_families_service(db: DataBaseDep) -> list[model.Family]:
    return await model.Family.get_multi(db)


async def get_family_service(db: DataBaseDep, query: dict) -> model.Family | None:
    return await model.Family.get(db, query)


async def create_family_service(
    db: DataBaseDep,
    family: model.FamilyCreate,
) -> InsertOneResultMongo:
    result = await model.Family.create(db, obj_to_create=family.model_dump())
    if not result.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )
    return result


async def delete_family_service(db: DataBaseDep, query: dict) -> model.Family:
    mongo_delete: DeleteResultMongo = await model.Family.delete(db, query)

    if mongo_delete.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found'
        )
    if not mongo_delete.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='DB error'
        )


async def update_family_service(
    db: DataBaseDep,
    family_id: UUID4,
    family_update: model.FamilyUpdate
) -> model.Family | None:
    return await model.Family.update(
        db,
        query={'id': family_id},
        data_to_update=family_update.model_dump()
    )


async def udpate_person_service(
    db: DataBaseDep,
    family_id: UUID4,
    person_nid: str,
    person: model.PersonUpdate
) -> model.Person | None:
    family = await model.Family.get(db, query={'id': family_id})
    old_person = [
        person for person in family.members if person.nid == person_nid][0]
    updated_person = model.Person(**person.dict())
    if family is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )
    family.members.remove(old_person)
    family.members.append(updated_person)
