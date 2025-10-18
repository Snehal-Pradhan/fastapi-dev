from fastapi.testclient import TestClient
from app.crud import app
client = TestClient(app)


def test_user_not_found():
    response = client.get("/users/a")
    assert response.status_code == 422