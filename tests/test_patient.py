from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_patients():
    response = client.get("/patients")
    assert response.status_code == 200