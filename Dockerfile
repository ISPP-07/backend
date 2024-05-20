FROM python:3.11-alpine

RUN pip install pipenv
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo

COPY . /app

WORKDIR /app  

ENV PYTHONPATH=/app \     
    STAGING=False \     
    PROJECT_NAME="mock-api" \     
    API_STR="/api/v1/" \     
    CYC_NGO=True \     
    ACAT_NGO=True \     
    SERVER_HOST="0.0.0.0" \     
    SERVER_PORT=8000 \     
    FIRST_SUPERUSER_USERNAME="root" \     
    FIRST_SUPERUSER_PASSWORD="rootpass" \     
    FIRST_SUPERUSER_EMAIL="root@root.com" \     
    BACKEND_CORS_ORIGINS='["http://host.docker.internal/", "http://host.docker.internal:8000/"]' \
    MONGO_HOST=host.docker.internal \    
    MONGO_USER=mongouser \     
    MONGO_PASSWORD=mongopass \     
    MONGO_DB=isppdb \     
    MONGO_PORT=27017

RUN pipenv install

CMD ["pipenv", "run", "python", "/app/src/main.py"]