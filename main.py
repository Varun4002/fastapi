from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int]=None

@app.get("/")
async def root():
    return {"message":"Welcome to root"}

@app.get("/posts")
async def getpost():
    return {"message":"here is the post"}

@app.post("/posts")
async def create_post(post:Post):
    print(post.title)
    print(post.published)
    print(post.rating)
    print(post.dict())
    return {"message":"sucessfully created post"}