from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from backend.api.models.models import TermPopTerm, TermPopAgg, Comment

def populate_termpop_agg(db: Session):
    """
    Populates the dwh.termpop_agg table with aggregated term occurrence data.
    
    Args:
        db (Session): SQLAlchemy database session.
    """
    # Step 1: Delete all existing records from TermPopAgg
    db.query(TermPopAgg).delete()
    db.commit()  # Commit the deletion to the database

    # Step 2: Aggregate data and prepare for insertion
    # Build the query to aggregate occurrences of terms in comments
    aggregated_data = (
        db.query(
            TermPopTerm.id.label('term_id'),
            extract('year', Comment.time).label('year'),
            extract('month', Comment.time).label('month'),
            extract('week', Comment.time).label('week'),
            func.count('*').label('occurrence_count')
        )
        .join(Comment, Comment.text.ilike(func.concat('%', TermPopTerm.term, '%')))
        .group_by(
            TermPopTerm.id,
            extract('year', Comment.time),
            extract('month', Comment.time),
            extract('week', Comment.time)
        )
        .order_by(
            TermPopTerm.id,
            extract('year', Comment.time),
            extract('month', Comment.time),
            extract('week', Comment.time)
        )
    )

    # Execute the query and fetch all results
    results = aggregated_data.all()

    # Step 3: Create TermPopAgg instances for bulk insertion
    term_pop_agg_entries = [
        TermPopAgg(
            term_id=row.term_id,
            year=int(row.year),
            month=int(row.month),
            week=int(row.week),
            occurrence_count=row.occurrence_count
        )
        for row in results
    ]

    # Step 4: Bulk insert the aggregated data into TermPopAgg
    db.bulk_save_objects(term_pop_agg_entries)
    db.commit()  # Commit the insertions to the database