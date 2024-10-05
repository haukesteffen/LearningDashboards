import os
from ..crud import crud
from ..schemas import schemas
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = f'postgresql://{os.environ["DBUSER"]}:{os.environ["DBPW"]}@localhost:5432/hndb'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/comment", response_model=schemas.CommentBase)
def read_comment(db: Session = Depends(get_db), comment_id: int = 100000):
    db_comment = crud.get_comment(db=db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment