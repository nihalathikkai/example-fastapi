import pytest
from fastapi.testclient import TestClient
from jose import jwt
from app import schemas
from app.config import settings


print("file: test_users")
    
    
def test_create_user(client: TestClient):
    response = client.post("/users/", json={'email':'user1@example.com', 'password':'string123'})
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert response.json().get('email') == 'user1@example.com'
    

def test_login_user(test_user, client: TestClient):
    response = client.post('/login/', data={'username':test_user['email'], 'password':test_user['password']})
    new_token = schemas.Token(**response.json())
    payload = jwt.decode(new_token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: int = payload.get('user_id')
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    assert id == test_user['id']
    
    
@pytest.mark.parametrize('email, password, status_code',[
    ('user1@example.com', 'wrongpassword', 403),
    ('wrongemail@example.com', 'string123', 403),
    ('wrongemail@example.com', 'wrongpassword', 403),
    (None, 'string123', 422),
    ('user1@example.com', None, 422)
])
def test_incorrect_login(test_user, client: TestClient, email, password, status_code):
    response = client.post('/login/', data={'username':email, 'password':password})
    assert response.status_code == status_code
    # assert response.json().get('detail') == 'Invalid Credentials'