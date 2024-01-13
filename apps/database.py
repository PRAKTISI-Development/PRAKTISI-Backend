from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeMeta = declarative_base()

try:
    engine.connect()
except OperationalError as e:
    print(f"Error connecting to the database: {e}")
    raise SystemExit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
