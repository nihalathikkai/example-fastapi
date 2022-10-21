from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Boiii"}

@app.get("/welcome")
def welcome():
    return {"message": "Welcome to FastAPI"}

@app.get("/posts")
def posts():
    return {"data": "Here are your POSTS"}