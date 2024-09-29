import os
from utils import crud, models, schemas
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = f'postgresql://{os.environ["DBUSER"]}:{os.environ["DBPW"]}@localhost:5432/hndb'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/comment/{comment_id}", response_model=list[schemas.CommentBase])
def read_comment(comment_id: int, db: Session = Depends(get_db), limit: int = 5):
    db_comments = crud.get_n_comments(db=db, comment_id=comment_id, limit=limit)
    if db_comments is None:
        raise HTTPException(status_code=404, detail="Comments not found")
    return db_comments