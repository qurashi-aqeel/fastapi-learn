from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, utils, oauth2


router = APIRouter(
    tags=["User Auth"]
)


@router.post('/login')
def user_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    found_user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Incorrect Credentials."}
        )
    
    if not utils.verify(user_credentials.password, found_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Incorrect Credentials."}
        )
        
    # Now that user is there and password is correct so we will Create a token

    access_token = oauth2.create_access_token(data={"user_id": found_user.id})

    return {"access_token": access_token, "token_type": "bearer"}
