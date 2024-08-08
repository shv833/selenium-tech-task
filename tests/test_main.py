from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_read_users(db_session):
    response = client.get("/")
    assert response.status_code == 200
    assert "User Information" in response.text
