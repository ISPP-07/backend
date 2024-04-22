import re
from typing import Optional

from fastapi import HTTPException, status
from pydantic import UUID4

from src.core.deps import DataBaseDep
from src.modules.cyc.family import model
from src.modules.cyc.family import service


async def get_families_controller(
    db: DataBaseDep,
    state: Optional[model.DerecognitionStatus],
    referred_organization: Optional[str],
    name: Optional[str],
    limit=100,
    offset=0
) -> model.GetFamilies:
    families = await service.get_families_service(
        db,
        ('derecognition_state', state.value if state is not None else state),
        (
            'referred_organization', {
                '$regex': re.compile(f'^{referred_organization}', re.IGNORECASE)
            } if referred_organization is not None else referred_organization
        ),
        (
            'name', {
                '$regex': re.compile(f'^{name}', re.IGNORECASE)
            } if name is not None else name
        ),
        limit=limit,
        skip=offset
    )
    return model.GetFamilies(
        elements=families,
        total_elements=await service.count_families_service(db, query={})
    )


async def create_family_controller(db: DataBaseDep, family: model.FamilyCreate) -> model.Family:
    if family.members is not None:
        persons = await service.get_members_service(db)
        for m in family.members:
            if m.nid is not None and any(
                    person.nid == m.nid for person in persons):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'There is already a person with this NID: {m.nid}',
                )
    mongo_insert = await service.create_family_service(db, family)
    result = await service.get_family_service(db, query={'id': mongo_insert.inserted_id})
    return result


async def get_family_details_controller(db: DataBaseDep, family_id: int) -> model.Family:
    result = await service.get_family_service(db, query={'id': family_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )
    return result


async def update_family_controller(db: DataBaseDep, family_id: UUID4, family: model.FamilyUpdate) -> model.Family:
    if family.members is not None:
        persons = await service.get_members_service(db)
        for m in family.members:
            if m.nid is not None and any(
                    person.nid == m.nid for person in persons):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'There is already a person with this NID: {m.nid}',
                )
    request_none_fields = [
        field for field in model.FAMILY_NONE_FIELDS
        if field in family.update_fields_to_none
    ]
    update_data = family.model_dump(exclude='update_fields_to_none')
    for field in update_data.copy():
        if field in request_none_fields:
            continue
        if update_data[field] is None:
            update_data.pop(field)
    result = await service.update_family_service(db, family_id=family_id, family_update=update_data)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )
    return result


async def delete_family_controller(db: DataBaseDep, family_id: UUID4):
    await service.delete_family_service(db, query={'id': family_id})


async def update_person_controller(db: DataBaseDep, family_id: UUID4, person_nid: str, person: model.PersonUpdate) -> model.Person:
    family = await service.get_family_service(db, query={'id': family_id})
    if family is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )
    old_person = next(
        (person for person in family.members if person.nid == person_nid),
        None
    )
    if old_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Person not found in family',
        )
    request_none_fields = [
        field for field in model.PERSON_NONE_FIELDS
        if field in person.update_fields_to_none
    ]
    update_data = person.model_dump(exclude=['update_fields_to_none'])
    old_person_data = old_person.model_dump()
    for field in old_person_data:
        if field in request_none_fields:
            continue
        if field not in update_data or update_data[field] is None:
            update_data[field] = old_person_data[field]
    members = [
        p.model_dump() for p in family.members
        if p.nid != old_person.nid
    ]
    members.append(update_data)
    return await service.update_family_service(
        db,
        family_id=family.id,
        family_update={'members': members}
    )


async def delete_person_controller(db: DataBaseDep, family_id: UUID4, person_nid: str) -> None:
    new_family = await service.get_family_service(db, query={'id': family_id})
    if new_family is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )

    if person_nid not in [person.nid for person in new_family.members]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Person not found in family',
        )

    head_person = [
        person for person in new_family.members if person.family_head
    ][0]
    if head_person.nid == person_nid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot delete the family head',
        )
    members = [
        person.model_dump() for person in new_family.members
        if person.nid != person_nid
    ]
    await service.update_family_service(
        db,
        family_id,
        family_update={'members': members}
    )
