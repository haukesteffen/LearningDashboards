import os
from backend.etl.dwh.update_dwh import populate_termpop_agg
from backend.api.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f'postgresql://{os.environ["DBUSER"]}:{os.environ["DBPW"]}@localhost:5432/hndb'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    try: 
        db = SessionLocal()
        populate_termpop_agg(db=db)
    finally:
        db.close()