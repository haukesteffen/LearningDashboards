from ..crud import crud
from ..schemas import schemas
from ..database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

page2_router = APIRouter()

@page2_router.get("/termpop/agg", response_model=List[schemas.TermPopAggBase])
def read_termpop_agg(
    term_id: int,
    agg: str = 'year',
    db: Session = Depends(get_db)
):
    # Validate the 'agg' parameter
    if agg not in ['year', 'month', 'week']:
        raise HTTPException(status_code=400, detail="Aggregation must be 'year', 'month', or 'week'.")

    # Retrieve aggregated data
    data = crud.get_termpop_agg(db=db, term_id=term_id, agg=agg)

    if not data:
        raise HTTPException(status_code=404, detail="No data found for the specified term_id and aggregation.")

    # Convert the query results to a list of TermAggregation instances
    aggregations = []
    for row in data:
        aggregation_data = {
            'year': row[0],
            'occurrence_count': row[-1]
        }
        if agg == 'month':
            aggregation_data['month'] = row[1]
        elif agg == 'week':
            aggregation_data['week'] = row[1]
        aggregations.append(schemas.TermPopAggBase(**aggregation_data))

    return aggregations


@page2_router.get("/termpop/terms", response_model=List[schemas.TermPopTermBase])
def read_termpop_terms(db: Session = Depends(get_db)):
    data = crud.get_termpop_terms(db=db)
    if not data:
        raise HTTPException(status_code=404, detail="No term data found.")
    return data
