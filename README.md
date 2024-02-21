# Harmony project backend

This is a [FastAPI](https://fastapi.tiangolo.com/) (Starlette + Pydantic) project configured with [SQLModel](https://sqlmodel.tiangolo.com/) (SQLAlchemy + Pydantic) as ORM and [Alembic](https://alembic.sqlalchemy.org/en/latest/) as database migration system.


## Getting Started

First, set up your own configuration file. You can take the `example.env` file as a guide. By default, if the configuration is not loaded as environment variables, they will be taken from the `.env` file in the main project directory.

With the above, you are ready to launch the development server:

```bash
python -m src.main
```

> Note: The above command launches the server on the host and port specified in the configuration.

To be able to work with databases in development, you must launch your own instance of postgres and enter the necessary configuration in the `.env` file.

> Note: You can launch a postgres instance in Docker from the specification in the devcontainers folder.

If you have followed the above steps, you are ready to start developing.

## An overview of the api

You can see documentation of all the endpoints available in the api, as well as test them manually by accessing the following path once the development server is deployed:

`http://host:port/docs`

> Note: Replace host and port depending on the configuration of your development environment.

## Creating models

SQLModel is a library for interacting with SQL databases from Python code, with Python objects. It is designed to be intuitive, easy to use, highly compatible, and robust.

SQLModel is based on Python type annotations, and powered by [Pydantic](https://docs.pydantic.dev/latest/sql) and [SQLAlchemy](https://www.sqlalchemy.org).

To learn more about the implementation of models access the following [link](https://sqlmodel.tiangolo.com/)

A base class has been implemented so that all models derived from it have a complete CRUD implementation by default.

## Working with migrations

Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine. For a detailed tutorial follow this [link](https://alembic.sqlalchemy.org/en/latest/tutorial.html).

In most cases, you will only need the following commands.

### Create a Migration Script

With the environment in place we can create a new revision, using `alembic revision`:

```bash
alembic revision --autogenerate -m "create account table"
```

### Running our First Migration

We now want to run our migration. Assuming our database is totally clean, it’s as yet unversioned. The alembic upgrade command will run upgrade operations, proceeding from the current database revision, in this example `None`, to the given target revision. We can specify `1975ea83b712` as the revision we’d like to upgrade to, but it’s easier in most cases just to tell it “the most recent”, in this case `head`:

```bash
alembic upgrade head
```

> Note: This is the command you should use to apply the migrations to the database.

