from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/vote',
    tags=["Vote"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote_post(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: schemas.UserRes = Depends(oauth2.get_current_user)
):
    post_exists = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if post_exists == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such post."
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )

    existing_vote = vote_query.first()

    def save_vote(message: str = "success"):
        vote_query.update(
            {
                "post_id": vote.post_id,
                "user_id": current_user.id,
                "direction": vote.direction
            },
            synchronize_session=False
        )
        db.commit()
        return {"message": message}

    if existing_vote == None:
        new_vote = models.Vote(
            user_id=current_user.id,
            post_id=post_exists.id,
            direction=vote.direction
        )
        db.add(new_vote)
        db.commit()
        return {"message": f"successfully { 'upvoted' if vote.direction == 1 else 'downvoted' }"}


    # vote.direction = new direction for vote
    match vote.direction: 
        case (0):
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "removed vote"}
        case -1:
            if bool(existing_vote.direction == -1):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Post already downvoted"
                )
            else:
                return save_vote("successfully downvoted")
        case 1:
            if bool(existing_vote.direction == 1):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Post already upvoted"
                )
            else:
                return save_vote("successfully upvoted")

    return existing_vote
