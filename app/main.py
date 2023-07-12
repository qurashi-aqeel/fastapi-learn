from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db, engine
from .utils import hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def root():
    return 'server is running...'


# Get all posts
@app.get('/posts', response_model=list[schemas.PostRes])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Create a post
@app.post(
    '/posts',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostRes
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db)
):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get single post
@app.get(
    '/posts/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostRes
)
def get_post(
    id: int,
    db: Session = Depends(get_db)
):
    matched_post = db.query(models.Post).filter(models.Post.id == id).first()

    if (matched_post):
        return matched_post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Post {id} not found."}
        )


# Delete a post
@app.delete(
    '/posts/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    id: int,
    db: Session = Depends(get_db)
):
    matched_post = db.query(models.Post).filter(
        models.Post.id == id).delete(synchronize_session=False)
    db.commit()

    if matched_post:
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"No such post found."}
        )


# Update a post
@app.put('/posts/{id}', response_model=schemas.PostRes)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    matched_post = post_query.first()

    if (matched_post):
        post_query.update(
            dict(post.model_dump()),
            synchronize_session=False
        )
        db.commit()
        return post_query.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"No such post found."}
        )


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserRes
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Hash the passwoed
    user.password = hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
