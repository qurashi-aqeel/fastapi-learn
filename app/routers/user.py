from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db
from ..utils import hash


router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

# create new user
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserRes
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    user_exists = db.query(models.User).filter(models.User.email == user.email).first()

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered."
        )
    
    # Hash the password
    user.password = hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get user info
@router.get('/{id}', response_model=schemas.UserRes)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)
):
    found_user = db.query(models.User).filter(models.User.id == id).first()

    if(found_user):
        return found_user
    
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"No such user found."}
        )

