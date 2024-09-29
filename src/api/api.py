import os
from typing import Union
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


@app.get("/latest/", response_model=Union[list[schemas.CommentBase], list[schemas.StoryBase], list[schemas.JobBase]])
def read_latest(db: Session = Depends(get_db), type: str = "Comment", limit: int = 5):
    # instantiate table object from string input
    table = getattr(models, type, None)
    if table is None:
        raise HTTPException(status_code=404, detail=f"Type '{type}' not found.")
    
    # run query
    db_latest = crud.get_latest(db=db, table=table, limit=limit)
    if db_latest is None:
        raise HTTPException(status_code=404, detail=type + " not found")
    return db_latest