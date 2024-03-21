from fastapi import HTTPException, status

from pydantic import UUID4
from src.core.deps import DataBaseDep
from src.modules.cyc.family import model
from src.modules.cyc.family import service


async def get_families_controller(db: DataBaseDep):
    return await service.get_families_service(db)


async def create_family_controller(db: DataBaseDep, family: model.FamilyCreate) -> model.Family:
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

async def update_person_controller(db: DataBaseDep, family_id: UUID4, person_nid: str, person: model.PersonUpdate) -> model.Family:
    family = await service.get_family_service(db, query={'id': family_id})
    if family is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )
    old_person = [person for person in family.members if person.nid == person_nid][0]
    if old_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Person not found in family',
        )
    
    if old_person.family_head == True and person.family_head == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot remove the family head',
        )
    updated_person = model.Person(
        nid=old_person.nid if person.nid is None else person.nid,
        date_birth=old_person.date_birth if person.date_birth is None else person.date_birth,
        type=old_person.type if person.type is None else person.type,
        name=old_person.name if person.name is None else person.name,
        family_head=old_person.family_head if person.family_head is None else person.family_head,
        surname=old_person.surname if person.surname is None else person.surname,
        nationality=old_person.nationality if person.nationality is None else person.nationality,
        gender=old_person.gender if person.gender is None else person.gender,
        functional_diversity=old_person.functional_diversity if person.functional_diversity is None else person.functional_diversity,
        food_intolerances=old_person.food_intolerances if person.food_intolerances is None else person.food_intolerances,
        homeless=old_person.homeless if person.homeless is None else person.homeless,
    )
    family.members.remove(old_person)
    new_persons = family.members + [updated_person]
    family.members = new_persons
    return await service.update_family_service(db,family_id=family.id, family_update=family)

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
    
    head_person = [person for person in new_family.members if person.family_head][0]
    if head_person.nid == person_nid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot delete the family head',
        )
    new_family.members = [person for person in new_family.members if person.nid != person_nid]
    await service.update_family_service(db, family_id, new_family)