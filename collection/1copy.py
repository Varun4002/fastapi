from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published :bool = True
    rating : Optional[int]=None

@app.get("/")
def root():
    return {"message":"Welcome to my api!!!"}

@app.get("/posts")
def get_posts():
    return {"message":"here is the posts"}

@app.post("/createpost")
def create_post(post:Post):
    print(post.published)
    print(post.rating)
    print(post.dict())  
    return {"message":f"title is {post.title} and content is {post.content } "}