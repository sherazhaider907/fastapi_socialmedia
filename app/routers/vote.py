from fastapi import Response, status, HTTPException, APIRouter , Depends

from .. import models, schemas , oauth2

# DB dependency shortcut
from ..dependencies import db_dependency


router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

# Create vote
@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: db_dependency, response: Response, current_user: int = Depends(oauth2.get_current_user)):

    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} does not exist")
    
    # Check if vote exists
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        # create vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully added vote"}
    else:
        # delete vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_200_OK
        return {"message": "successfully deleted vote"}
