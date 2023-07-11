from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time


# Pydantic Post model
class Post(BaseModel):
    title: str
    content: str
    draft: bool = False


while True:
    try:
        conn = psycopg.connect(
            host="localhost", dbname="fastapi-learn",
            user="postgres", password="password"
        )
        print("DB connected.")
        cur = conn.cursor(row_factory=dict_row)

        # cur.execute("SELECT * FROM posts")
        # results = cur.fetchall()
        # print(results)

        break

    except Exception as error:
        print("Failed connecting to DB", error)
        time.sleep(2)


app = FastAPI()

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 173},
    {"title": "favorite foods", "content": "I like pizza", "id": 287}
]


def find_post(id):
    matched_post = None

    for post in my_posts:
        if post['id'] == id:
            matched_post = post

    return matched_post


@app.get('/')
def root():
    return 'server is running...'


# Get all posts
@app.get('/posts')
def get_posts():
    posts = cur.execute("SELECT * FROM posts").fetchall()
    return {"data": posts}


# Create a post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    new_post = cur.execute(
        f"INSERT INTO posts (title, content, draft) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.draft)).fetchone()
    conn.commit()
    return {"data": new_post}


# Get single post
@app.get('/posts/{id}')  # id is always a string.
async def get_post(id: int, response: Response):
    matched_post = cur.execute(
        "SELECT * FROM posts WHERE id=%s", (id,)).fetchone()

    if (matched_post):
        response.status_code = status.HTTP_200_OK
        return {"data": matched_post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post {id} not found."})
        # response.status_code = 404
        # return {"data": {"error": "No such post"}}


# Delete a post
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cur.execute("DELETE FROM posts WHERE id=%s RETURNING title", (id,))
    conn.commit()

    if cur.rowcount:
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"No such post found."})

# Update a post


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    updated_post = cur.execute(
        "UPDATE posts SET title = %s, content = %s, draft = %s WHERE id=%s RETURNING *", (post.title, post.content, post.draft, id)).fetchone()
    conn.commit()

    if (updated_post):
        return {"Updated": updated_post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"No such post found."})
