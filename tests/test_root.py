from fastapi.testclient import TestClient


def test_root(client: TestClient):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'Welcome to FastAPI !!!'