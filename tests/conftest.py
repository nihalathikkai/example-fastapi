import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db 
from app import models
from app.oauth2 import create_access_token


print("file: test/database")

## setup testing database
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   

@pytest.fixture()
def db():
    print("fixture: db")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db):
    print("fixture: client")
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def test_user(client: TestClient):
    user_data = {'email':'user1@example.com', 'password':'string123'}
    response = client.post('/users/', json=user_data)
    new_user = response.json()
    new_user['password'] = user_data['password']
    assert response.status_code == 201
    return new_user


@pytest.fixture()
def test_user2(client: TestClient):
    user_data = {'email':'user2@example.com', 'password':'string123(2)'}
    response = client.post('/users/', json=user_data)
    new_user = response.json()
    new_user['password'] = user_data['password']
    assert response.status_code == 201
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    # client.headers = {**client.headers, 'Authorization': f"Bearer {token}"}
    client.headers['Authorization']= f"Bearer {token}"
    return client


@pytest.fixture()
def test_posts(test_user: dict, test_user2: dict, db: Session):
    data = [{
        'title':'title #1',
        'content':'content #1',
        'owner_id':test_user['id']
    }, {
        'title':'title #2',
        'content':'content #2',
        'owner_id':test_user['id']
    }, {
        'title':'title #3',
        'content':'content #3',
        'owner_id':test_user['id']
    }, {
        'title':'title #4',
        'content':'content #4',
        'owner_id':test_user2['id']
    }]
    db.add_all([models.Post(**_) for _ in data])
    db.commit()
    new_posts = db.query(models.Post).all()
    return new_posts
    