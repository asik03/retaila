from starlette.testclient import TestClient

from app.api.v1.v1 import api_v1

client = TestClient(api_v1)


def test_ping():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}





