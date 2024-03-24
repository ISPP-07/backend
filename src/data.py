import argparse
import asyncio
import json

from motor.motor_asyncio import AsyncIOMotorClient

from src.core.database import backup


async def populate_json_data(motor: AsyncIOMotorClient, route: str):
    try:
        with open(route, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(
                data,
                dict) or not all(
                isinstance(
                    value,
                    list) for value in data.values()):
                raise ValueError("Invalid JSON data format")
            await backup.populate_from_json(motor, data)
    except FileNotFoundError:
        print(f"File not found: {route}")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file: {route}")
    except ValueError as e:
        print(f"Invalid JSON data format: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


async def dump_json_data(motor: AsyncIOMotorClient, route: str):
    try:
        data = await backup.dump_to_json(motor)
        with open(route, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, cls=backup.BackupEncoder)
            print(f"Data dumped to file: {route}")
    except Exception as e:
        print(f"An error occurred: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Dump or retrieve JSON data")
    parser.add_argument("option", choices=[
                        "dump", "populate"], help="Dump or retrieve JSON data")
    parser.add_argument("route", help="File route")

    args = parser.parse_args()

    db = await backup.get_database_session()
    client = db.client
    if args.option == "dump":
        await dump_json_data(db, args.route)
    elif args.option == "populate":
        await populate_json_data(db, args.route)

    client.close()

if __name__ == "__main__":
    asyncio.run(main())
