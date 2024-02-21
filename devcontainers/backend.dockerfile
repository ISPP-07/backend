FROM python:3.11-alpine

RUN pip install pipenv
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo

WORKDIR /app

COPY Pipfile Pipfile.lock alembic.ini ./
COPY src ./src
COPY migrations ./migrations

RUN pipenv install
