from random import randint
import pytest
from typing import List
from fastapi.testclient import TestClient
from app import schemas


def test_get_all_posts(authorized_client: TestClient, test_posts):
    response = authorized_client.get('/posts/')
    posts = [schemas.PostResponse(**_) for _ in response.json()]
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)
    assert posts[0].Post.id == test_posts[0].id
    
    
def test_unauthorized_user_get_all_posts(client: TestClient, test_posts):
    response = client.get('/posts/')
    assert response.status_code == 401
    
    
def test_get_one_post(authorized_client: TestClient, test_posts):
    response = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostResponse(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.owner_id == test_posts[0].owner_id
    
    
def test_get_one_post_not_exists(authorized_client: TestClient, test_posts):
    rand_id = randint(0,10000)
    while rand_id in [_.id for _ in test_posts]:
        rand_id = randint(0,10000)
    response = authorized_client.get(f'/posts/{rand_id}')
    assert response.status_code == 404


def test_unauthorized_user_get_one_post(client: TestClient, test_posts):
    response = client.get(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401
    
    
@pytest.mark.parametrize("title, content, publish", [
    ('Lorem ipsum', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer neque sem, volutpat eu enim eu, porta ultrices tortor.', True),
    ('new title', 'new content', False),
    ('121211@$#^#!#', '09096757456', True)
])
def test_create_post(title, content, publish, authorized_client: TestClient, test_user, test_posts):
    data = {
        'title':title,
        'content':content,
        'publish':publish
    }
    response = authorized_client.post('/posts/', json = data)
    post = schemas.PostOut(**response.json())
    assert response.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.publish == publish
    assert post.owner_id == test_user['id']
    

def test_create_post_default_publish(authorized_client: TestClient, test_user, test_posts):
    data = {
        'title':"Test title",
        'content':"Test post contents"
    }
    response = authorized_client.post('/posts/', json = data)
    post = schemas.PostOut(**response.json())
    assert response.status_code == 201
    assert post.title == data['title']
    assert post.content == data['content']
    assert post.publish == True
    assert post.owner_id == test_user['id']
    
    
def test_unauthorized_user_create_post(client: TestClient):
    data = {
        'title':"Test title",
        'content':"Test post contents"
    }
    response = client.post('/posts/', json = data)
    assert response.status_code == 401
    
    
def test_delete_post(authorized_client: TestClient, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 204
    
    
def test_delete_post_not_exists(authorized_client: TestClient, test_posts):
    rand_id = randint(0,10000)
    while rand_id in [_.id for _ in test_posts]:
        rand_id = randint(0,10000)
    response = authorized_client.delete(f'/posts/{rand_id}')
    assert response.status_code == 404
    

def test_delete_other_user_post(authorized_client: TestClient, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert response.status_code == 403
    
    
def test_unauthorized_user_delete_post(client: TestClient, test_posts):
    response = client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_update_post_no_data_sent(authorized_client: TestClient, test_posts):
    response = authorized_client.put(f'/posts/{test_posts[0].id}', json={})
    assert response.status_code == 400
    
    
def test_update_post_title(authorized_client: TestClient, test_posts):
    data = {'title':'Updated title',
            'content':'Updated Content'}
    response = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    post = schemas.PostOut(**response.json())
    assert response.status_code == 202
    assert post.title == 'Updated title'
    
    
def test_update_post_not_exists(authorized_client: TestClient, test_posts):
    rand_id = randint(0,10000)
    while rand_id in [_.id for _ in test_posts]:
        rand_id = randint(0,10000)
    data = {'title':'Updated title',
            'content':'Updated Content'}
    response = authorized_client.put(f'/posts/{rand_id}', json=data)
    assert response.status_code == 404
    

def test_update_other_user_post(authorized_client: TestClient, test_posts):
    data = {'title':'Updated title',
            'content':'Updated Content'}
    response = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)
    assert response.status_code == 403
    
    
def test_unauthorized_user_update_post(client: TestClient, test_posts):
    data = {'title':'Updated title',
            'content':'Updated Content'}
    response = client.put(f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 401