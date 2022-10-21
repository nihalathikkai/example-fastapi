import imp
from random import randrange
from time import sleep
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# creating a pydantic data structure for posts
class Post(BaseModel):  
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None
    

# Connect to an existing database
while True:
    try:
        conn = psycopg2.connect(dbname="fastapi", user="postgres", password="superuser", host="localhost", port=5432, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("database connection was successful")
        break
    except Exception as error:
        print("database connection failed")
        print("Error: ", error)
        sleep(2)


# initialising FastAPI object
app = FastAPI()


@app.get("/")
def root():
    print("root")
    return {"message": "Welcome to FastAPI"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(data: Post):
    print("create_post")
    cur.execute("INSERT INTO posts (title, content, publish) VALUES (%s, %s, %s) RETURNING *", (data.title, data.content, data.publish))
    res = cur.fetchone()
    if data.rating != None:
        id = res['id']
        cur.execute("UPDATE posts SET rating=%s WHERE id=%s RETURNING *", (data.rating, id))
        res = cur.fetchone()
    conn.commit()
    return {"data": res}


@app.get("/posts")
def get_all_posts():
    print("get_all_posts")
    cur.execute("SELECT * FROM posts")
    res = cur.fetchall()
    return {"data": res}


@app.get("/posts/latest")
def get_latest_post():
    print("get_latest_post")
    cur.execute("SELECT * FROM posts WHERE id=(SELECT MAX(id) FROM posts)")
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No posts found")
    return {"data": res}


@app.get("/posts/{id}")
def get_one_post(id: int):
    print("get_one_post")
    cur.execute("SELECT * FROM posts WHERE id=%s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {"data": res}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    print("delete_post")
    cur.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    conn.commit()
    return {"message": "post was successfully deleted", 
            "deleted" : res}
    
    
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_posts(id: int, data: Post):
    print("update_post")
    print(data)
    cur.execute("UPDATE posts SET title=%s, content=%s, publish=%s WHERE id=%s RETURNING *", (data.title, data.content, data.publish, id))
    if data.rating != None: 
        cur.execute("UPDATE posts SET rating=%s WHERE id=%s RETURNING *", (data.rating, id))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    conn.commit()
    return {"data": res}