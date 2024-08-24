from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, auth2, models

router = APIRouter(prefix="/vote", tags=['Votes'])


@router.post('/')
def vote(vote_post: schemas.Vote,
         db: Session = Depends(database.get_db),
         current_user: int = Depends(auth2.get_current_user)):

    # Does post exist
    post_exist = db.query(models.Post).filter(models.Post.id == vote_post.post_id).first()

    if post_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id {vote_post.post_id} does not exist")


    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote_post.post_id)
    vote_exist = vote_query.first()
    if vote_exist:
        return {'message': f"you have already vote post {vote_post.post_id}"}
    # like
    if vote_exist is None and vote_post.vote_dir == 1:
        new_vote = models.Vote(user_id=current_user.id, post_id=vote_post.post_id)
        db.add(new_vote)
        db.commit()

    # dislike
    if vote_exist is not None and vote_post.vote_dir == 0:
        vote_query.delete(synchronize_session=False)
        db.commit()

    return {"message": "successful update"}
