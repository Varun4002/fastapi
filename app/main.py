from random import randrange
from typing import Optional
from fastapi import Body, FastAPI , Response , status ,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine

app = FastAPI()



SQLModel.metadata.create_all(engine)

my_Posts = [{"title":"title of post 1","content":"content of post 1","id":1},
            {"title":"title of post 2","content":"content of post 2","id":2}]

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='12345',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to DB")
        break

    except Exception as e:
        print("Connection failed")
        print("reason",e)

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

@app.get("/")
def root():
    
    return {"message":"WELCOME TO ROOT"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    post = cursor.fetchall()
    return {"data":post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'message':new_post}

@app.get("/posts/{id}")
def get_post(id:str,responce :Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id:{id} was not found")
        # responce.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"the id:{id} was not found"}
    return {"message":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""",(str(id),))
    Post=cursor.fetchone()
    conn.commit()
    if Post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found post")
    return {"message":"post was removed sucessfully"}

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    post =cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post wit id {str(id)} was not found")
    return{"message":post}
