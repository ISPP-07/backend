import asyncio
from src.core.database.initialise import init_db
from src.core.database.session import SessionLocal


async def create_init_data() -> None:
    async with SessionLocal() as session:
        await init_db(session)


async def main() -> None:
    await create_init_data()


if __name__ == "__main__":
    asyncio.run(main())
