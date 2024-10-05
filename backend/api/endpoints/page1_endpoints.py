from ..crud import crud
from ..schemas import schemas
from ..database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

page1_router = APIRouter()

@page1_router.get("/comment", response_model=schemas.CommentBase)
def read_comment(db: Session = Depends(get_db), comment_id: int = 100000):
    db_comment = crud.get_comment(db=db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment