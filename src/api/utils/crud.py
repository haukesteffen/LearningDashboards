from typing import Union
from sqlalchemy.orm import Session
from sqlalchemy import desc, extract, func
from . import models, schemas

def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def get_n_comments(db: Session, comment_id: int, limit: int):
    return db.query(models.Comment) \
        .filter(models.Comment.id <= comment_id) \
        .order_by(desc(models.Comment.id)) \
        .limit(limit=limit) \
        .all()

def get_latest(db: Session, table: Union[schemas.CommentBase, schemas.StoryBase, schemas.JobBase], limit: int):    
    return db.query(table) \
        .order_by(desc(table.id)) \
        .limit(limit=limit) \
        .all()

def get_popularity_by_year(db: Session, string: str):
    subquery = db.query(
            extract('year', models.Comment.time).label('year')
        ).filter(
            func.lower(models.Comment.text).like(func.lower(f'%{string}%'))
        ).subquery()
    query = db.query(
        subquery.c.year.label('year'),
        func.count().label('count')
    ).group_by(
        subquery.c.year
    ).all()
    return query