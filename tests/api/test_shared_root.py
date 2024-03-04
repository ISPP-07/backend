from fastapi.testclient import TestClient
from src.core.config import settings


def test_root(client: TestClient):
    url = f'{settings.API_STR}shared/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.text == '"Hello from root service!"'
