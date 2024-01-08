from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from apps.models.user import User
from apps.models.praktikan import Praktikan

def create_praktikan(db: Session, praktikan_data: Praktikan):
    db_praktikan = Praktikan(**praktikan_data.dict())
    db.add(db_praktikan)
    db.commit()
    db.refresh(db_praktikan)
    return db_praktikan

def get_praktikan(db: Session, nim: str):
    return db.query(Praktikan).filter(Praktikan.nim == nim).first()

def get_praktikans(db: Session):
    return db.query(Praktikan).all()

def update_praktikan(db: Session, nim: str, praktikan_data: Praktikan):
    db_praktikan = db.query(Praktikan).filter(Praktikan.nim == nim).first()
    for key, value in praktikan_data.dict().items():
        setattr(db_praktikan, key, value)
    db.commit()
    db.refresh(db_praktikan)
    return db_praktikan

def delete_praktikan(db: Session, nim: str):
    db_praktikan = db.query(Praktikan).filter(Praktikan.nim == nim).first()
    db.delete(db_praktikan)
    db.commit()
    return {"message": "Praktikan deleted successfully"}
