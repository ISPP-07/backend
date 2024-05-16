# Harmony project backend

This is a [FastAPI](https://fastapi.tiangolo.com/) (Starlette + Pydantic) project configured with [MongoDB](https://www.mongodb.com/es) as database migration system.


## Getting Started

First, set up your own configuration file. You can take the `example.env` file as a guide. By default, if the configuration is not loaded as environment variables, they will be taken from the `.env` file in the main project directory.

The next step will be to download and install [MongoDB](https://www.mongodb.com/try/download/community) and configure it so you can make requests to the database.

Once you are done with it, you will need to install **pipenv** if you haven't done it already and run **pipenv install** in your terminal, so you can download the dependencies of the project. If you don't have a virtual environment previously created you don't have to worry about it, since pipenv will create a folder in your computer in which these dependencies will be hosted.

With the above, you are ready to launch the development server:

```bash
pipenv run python -m src.main
```

> Note: The above command launches the server on the host and port specified in the configuration.

To be able to work with databases in development, you must launch your own instance of mongo and enter the necessary configuration in the `.env` file.

> Note: You can launch a mongo instance in Docker from the specification in the devcontainers folder.

If you have followed the above steps, you are ready to start developing.

### Docker

To launch the backend locally with Docker you must change the Dockerfile environment variables: `MONGO_USER`, `MONGO_PASSWORD` and `MONGO_DB`. Then run command: `docker-compose up`. With this you can browse to localhost:8000/docs to see the swagger

## An overview of the api

You can see documentation of all the endpoints available in the api, as well as test them manually by accessing the following path once the development server is deployed:

`http://host:port/docs`

> Note: Replace host and port depending on the configuration of your development environment.
