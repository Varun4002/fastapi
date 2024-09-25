from random import randrange
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel


app = FastAPI()

my_Posts = [{"title":"title of post 1","content":"content of post 1","id":1},
            {"title":"title of post 2","content":"content of post 2","id":2}]

def find_post(id):
    for p in my_Posts:
        if p["id"]==id:
            return p

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
    return {"data":my_Posts}

@app.post("/posts")
def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"]=randrange(0,1000000000000000000000)
    my_Posts.append(post_dict)
    my_Posts.append(post.dict())
    return {'message':post_dict}

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    return {"message":post}
