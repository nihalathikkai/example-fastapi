from random import randrange
from typing import Optional
from xmlrpc.client import boolean
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    

my_posts = [{"title": "Title of post 1", 
             "content": "Content of post 1", 
             "id": 1},
            {"title": "title of post 2",
             "content": "Content of post 2",
             "id": 2}]


def find_post(id):
    for post in my_posts:
        if post["id"]==id:
            return post
    return "404"

@app.get("/")
async def root():
    return {"message": "Welcome to new API"}


@app.get("/posts")
def get_posts():
    return {"data" : my_posts}


@app.post("/posts")
def create_post(post: Post):
    print(post)
    post_dict = post.dict()   # Convert pydantic to dict
    print(post_dict)
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    print(id, type(id))
    post = find_post(id)
    return {"data": post}