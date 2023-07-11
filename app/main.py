from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


# Get single post
@app.get('/posts/{id}', status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):
    matched_post = db.query(models.Post).filter(models.Post.id == id).first()

    if (matched_post):
        return {"data": matched_post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Post {id} not found."}
        )


# Delete a post
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
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
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if (post_to_update):
        post_query.update(dict(post.model_dump()), synchronize_session=False)
        db.commit()
        return {"Updated": post_query.first()}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"No such post found."})
