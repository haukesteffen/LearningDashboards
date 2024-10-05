from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models import models

def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def get_termpop_agg(db: Session, term_id: int, agg: str = 'year'):
    assert agg in ['year', 'month', 'week']

    if agg == 'year':
        group_by_columns = [models.TermPopAgg.year]
    elif agg == 'month':
        group_by_columns = [models.TermPopAgg.year, models.TermPopAgg.month]
    elif agg == 'week':
        group_by_columns = [models.TermPopAgg.year, models.TermPopAgg.week]
    
    results = (
        db.query(
            *group_by_columns,
            func.sum(models.TermPopAgg.occurrence_count).label('occurrence_count')
        )
        .filter(models.TermPopAgg.term_id == term_id)
        .group_by(*group_by_columns)
        .order_by(*group_by_columns)
        .all()
    )

    return results

def get_termpop_terms(db: Session):
    return db.query(models.TermPopTerm).all()