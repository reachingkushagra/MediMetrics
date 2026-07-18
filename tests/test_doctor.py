from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_doctors():
    response = client.get("/doctors")
    assert response.status_code == 200
