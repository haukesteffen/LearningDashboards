from sqlalchemy.orm import Session
from . import models

def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()