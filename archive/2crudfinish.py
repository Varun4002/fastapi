from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, HTTPException , Response ,status
from pydantic import BaseModel

app = FastAPI()

my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},
            {"title":"title of post 2","content":"content of post 2","id":2}]

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int]=None

def find_Post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p  in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message":"Welcome to root"}

@app.get("/posts")
async def getpost():
    return {"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"]= randrange(0,10000000000)
    my_posts.append(post.dict())
    return {"message":"sucessfully created post"}

@app.get("/posts/latest")
async def latest():
    post = my_posts[-1]
    print(post)
    return {"message": post} 

@app.get("/posts/{id}")
async def get_post(id:int,responce : Response):
    print(id)
    post = find_Post(id)
    if not post:
        # responce.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":"Post doesnt exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id {id} not found")
    return {"message":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_Post(id:int,post :Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    return {"message":"updated post"}

