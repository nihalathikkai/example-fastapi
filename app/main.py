from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from . import models
# from .database import engine
from .routers import post, user, auth, vote


print("file: main")

# models.Base.metadata.create_all(bind=engine)

# initialising FastAPI object
app = FastAPI()

origins = ["*"]   # for all domiains to access.
# origins = ['https://www.google.com', 'https://www.youtube.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    print("root")
    return {"message": "Welcome to FastAPI !!!",
            "deployed from": "CI/CD pipeline"}