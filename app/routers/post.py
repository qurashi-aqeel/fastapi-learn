from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .. import oauth2


router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


# Get all posts
@router.get('/', response_model=list[schemas.PostRes])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Create a post
@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostRes
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserRes = Depends(oauth2.get_current_user)
):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get single post
@router.get(
    '/{id}',
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
@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserRes = Depends(oauth2.get_current_user)
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
@router.put('/{id}', response_model=schemas.PostRes)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserRes = Depends(oauth2.get_current_user)
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
