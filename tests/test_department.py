from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_departments():
    response = client.get("/departments")
    assert response.status_code == 200