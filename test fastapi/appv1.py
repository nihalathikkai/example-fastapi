from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
# from fastapi.params import Body
from pydantic import BaseModel


# creating a pydantic data structure for posts
class Post(BaseModel):  
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None
    

# some hardcoded posts
my_posts = {
    1: {
        "title": "Title fpr post 1",
        "content": "Content for post 1",
        "id": 1
    },
    2: {
        "title": "Title fpr post 2",
        "content": "Content for post 2",
        "id": 2
    }
}

last_id = 2


# initialising FastAPI object
app = FastAPI()


@app.get("/")
def root():
    print("root")
    return {"message": "Welcome to FastAPI"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(data: Post): #, data: dict = Body(...), response: Response):
    print("create_post")
    post = data.dict()
    global last_id
    while last_id in my_posts:
        last_id = randrange(1,10000)
    post["id"] = last_id
    my_posts[last_id] = post
    # response.status_code = 201
    return {"data": my_posts[last_id]}


@app.get("/posts")
def get_all_posts():
    print("get_all_posts")
    return {"data": list(my_posts.values())}


@app.get("/posts/latest")
def get_latest_post():
    print("get_latest_post")
    if last_id not in my_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="latest post was deleted")
    return {"data": my_posts[last_id]}


@app.get("/posts/{id}")
def get_one_post(id: int): #, response: Response):
    print("get_one_post")
    if id not in my_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return {"data": my_posts[id]}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    print("delete_post")
    if id not in my_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"message": "post was successfully deleted", 
            "deleted" : my_posts.pop(id)}
    
    
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_posts(id: int, data: Post):
    print(data)
    if id not in my_posts:
        raise HTTPException(status_code=404,
                            detail=f"post with id {id} was not found")
    my_posts[id] = data.dict()
    return {"data": my_posts[id]}