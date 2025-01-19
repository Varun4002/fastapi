from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str

@app.get("/")
async def root():
    return {"message":"Welcome to root"}

@app.get("/posts")
async def getpost():
    return {"message":"here is the post"}

@app.post("/posts")
async def create_post(post:Post):
    print(post)
    return {"message":"sucessfully created post"}