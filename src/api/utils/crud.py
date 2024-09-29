from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models

def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def get_n_comments(db: Session, comment_id: int, limit: int):
    return db.query(models.Comment) \
            .filter(models.Comment.id <= comment_id) \
            .order_by(desc(models.Comment.id)) \
            .limit(limit=limit) \
            .all()