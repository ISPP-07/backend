from sqlmodel import select
from src.modules.cyc.family.model import Family, FamilyObservation, Person


async def get_families_service(session):
    return await Family.get_multi(session)


async def create_family_service(session, family: Family):
    obj = await Family.create(session, **family.model_dump())
    return obj


async def get_family_details_service(session, family_id: int):
    # Consulta para obtener los observation_text asociados al family_id
    observation_query = select(FamilyObservation.observation_text).where(
        FamilyObservation.family_id == family_id)

    person_query = select(Person).where(Person.family_id == family_id)

    # header_query = select(Person).where(
    #    Person.family_id == family_id, Person.family_header == True)

    # Ejecutar la consulta
    result = await session.execute(observation_query)
    result_person = await session.execute(person_query)
    # result_header = await session.execute(header_query)

    # Extraer los observation_text de los resultados
    observation_texts = [row[0] for row in result.fetchall()]
    persons = [p[0] for p in result_person.fetchall()]
    # header = [h[0] for h in result_header.fetchall()]

    family = await Family.get(session, id=family_id)

    json = family.model_dump()
    json["observations"] = observation_texts
    json["members"] = persons
    # json["family_head"] = header[0]

    return json
