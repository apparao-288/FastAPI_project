from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DB_URL = 'postgresql://postgres:9949764365@127.0.0.1:5432/users'
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
