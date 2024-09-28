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

@app.get("/comment/{comment_id}", response_model=schemas.CommentBase)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment