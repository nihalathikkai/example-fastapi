from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Welcome to new API"}


@app.get("/posts")
def get_posts():
    return {"data" : "my_posts"}


@app.post("/posts")
def create_post(post: Post):
    print(post)
    print(type(post))
    post.dict()   # Convert pydantic to dict
    return {"data": post}
    # return {"new_post" : f"Title: {new_post.title} ,Content: {new_post.content}"}
    

@app.post("/posts")
def create_post(post: dict = Body(...)):
    print(post)
    return {"new_post" : f"Title: {post['title']}, Content: {post['content']}"}