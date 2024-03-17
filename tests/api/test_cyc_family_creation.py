from fastapi.testclient import TestClient
from src.core.config import settings


def test_create_family(app_client: TestClient):
    url = f'{settings.API_STR}cyc/family/'
    family_data = {
        "name": "La Familia Pérez",
        "phone": "123456789",
        "address": "456 Main St",
        "referred_organization": "Hospital XYZ",
        "next_renewal_date": "2025-12-31",
        "observation": "Una observación",
        "members": [
            {
                "date_birth": "1985-08-25",
                "type": "Adult",
                "name": "Maria",
                "surname": "Pérez",
                "nationality": "Española",
                "nid": "51506994N",
                "family_head": True,
                "gender": "Woman",
                "functional_diversity": False,
                "food_intolerances": [],
                "homeless": False
            }
            # Puedes añadir más miembros según sea necesario
        ]
    }

    response = app_client.post(url=url, json=family_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == family_data["name"]
    assert response_data["address"] == family_data["address"]
