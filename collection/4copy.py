from random import randrange
from typing import Optional
from fastapi import Body, FastAPI , Response , status ,HTTPException
from pydantic import BaseModel


app = FastAPI()

my_Posts = [{"title":"title of post 1","content":"content of post 1","id":1},
            {"title":"title of post 2","content":"content of post 2","id":2}]

def find_post(id):
    for p in my_Posts:
        if p["id"]==id:
            return p
    
def find_index(id:int):
    for i,p in enumerate(my_Posts):
        if p["id"] == id:
            return i
    



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

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"]=randrange(0,1000000000000000000000)
    my_Posts.append(post_dict)
    my_Posts.append(post.dict())
    return {'message':post_dict}

@app.get("/posts/{id}")
def get_post(id:int,responce :Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} was not found")
        # responce.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"the id:{id} was not found"}
    return {"message":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index=find_index(id)
    my_Posts.pop(index)
    return {"message":"post was removed sucessfully"}