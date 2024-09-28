from random import randrange
from typing import Optional
from fastapi import Body, FastAPI , Response , status ,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='12345',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB CONNECTED")
        break

    except Exception as error:
        print("connection failed ",error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message":"WELCOME TO ROOT"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    post=cursor.fetchall()
    print(post)
    return {"data":post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (content,title,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post =  cursor.fetchone()
    conn.commit()
    return {'message':new_post}

@app.get("/posts/{id}")
def get_post(id:int,responce :Response):
    cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    found_post = cursor.fetchone()
    print(found_post)
    return {"message":found_post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index=find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found post")
    my_Posts.pop(index)
    return {"message":"post was removed sucessfully"}

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    index=find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found post")
    post_dict = post.dict()
    post_dict["id"]=id
    my_Posts[id]=post_dict
    return{"message":post}
