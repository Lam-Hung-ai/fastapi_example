from .. import schemas, models, auth2
from .. database import get_db
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user), limit: int = 10, skip: int = 0
              , search: Optional[str] = ""):

    result = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("Votes")
    ).join(
        models.Vote,
        models.Post.id == models.Vote.post_id,
        isouter=True
    ).group_by(
        models.Post.id
    ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), response_model=schemas.Post, current_user: int = Depends(auth2.get_current_user)):
    post = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("Votes")
    ).join(
        models.Vote,
        models.Post.id == models.Vote.post_id,
        isouter=True
    ).group_by(
        models.Post.id
    ).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post= post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"post is not your own")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    update_post = db.query(models.Post).filter(models.Post.id == id)
    post_ud = update_post.first()
    if post_ud is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post id {id} doesn't exist")
    if post_ud.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="post is not your own")
    update_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return update_post.first()
