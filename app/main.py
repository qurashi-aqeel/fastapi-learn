from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session

from . import models
from .database import get_db, engine


models.Base.metadata.create_all(bind=engine)


# Pydantic Post model
class Post(BaseModel):
    title: str
    content: str
    draft: bool = False


# while True:
#     try:
#         conn = psycopg.connect(
#             host="localhost", dbname="fastapi-learn",
#             user="postgres", password="password"
#         )
#         print("DB connected.")
#         cur = conn.cursor(row_factory=dict_row)

#         break

#     except Exception as error:
#         print("Failed connecting to DB", error)
#         time.sleep(2)


app = FastAPI()


@app.get('/alchemy')
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get('/')
def root():
    return 'server is running...'


# Get all posts
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# Create a post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    # `**post.model_dump()`: unpacks dict - post in required format
    # title=post.title, content=post.content, draft=post.draft
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


# Get single post
@app.get('/posts/{id}')
async def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # matched_post = cur.execute(
    #     "SELECT * FROM posts WHERE id=%s", (id,)).fetchone()

    matched_post = db.query(models.Post).filter(models.Post.id == id).first()

    if (matched_post):
        response.status_code = status.HTTP_200_OK
        return {"data": matched_post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post {id} not found."})


# Delete a post
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cur.execute("DELETE FROM posts WHERE id=%s RETURNING title", (id,))
    # conn.commit()

    matched_post = db.query(models.Post).filter(
        models.Post.id == id).delete(synchronize_session=False)
    db.commit()

    if matched_post:
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"No such post found."})

# Update a post


@app.put('/posts/{id}')
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # updated_post = cur.execute(
    #     "UPDATE posts SET title = %s, content = %s, draft = %s WHERE id=%s RETURNING *", (post.title, post.content, post.draft, id)).fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if (post_to_update):
        post_query.update(dict(post.model_dump()), synchronize_session=False)
        db.commit()
        return {"Updated": post_query.first()}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"No such post found."})
