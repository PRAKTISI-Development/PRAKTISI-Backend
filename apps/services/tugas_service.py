from sqlalchemy.orm import Session
from apps.models import Tugas

def create_tugas(db: Session, tugas_data: Tugas):
    db_tugas = Tugas(**tugas_data.dict())
    db.add(db_tugas)
    db.commit()
    db.refresh(db_tugas)
    return db_tugas

def get_tugas(db: Session, kode_tugas: str):
    return db.query(Tugas).filter(Tugas.kode_tugas == kode_tugas).first()

def get_tugass(db: Session):
    return db.query(Tugas).all()

def update_tugas(db: Session, kode_tugas: str, tugas_data: Tugas):
    db_tugas = db.query(Tugas).filter(Tugas.kode_tugas == kode_tugas).first()
    for key, value in tugas_data.dict().items():
        setattr(db_tugas, key, value)
    db.commit()
    db.refresh(db_tugas)
    return db_tugas

def delete_tugas(db: Session, kode_tugas: str):
    db_tugas = db.query(Tugas).filter(Tugas.kode_tugas == kode_tugas).first()
    db.delete(db_tugas)
    db.commit()
    return {"message": "Tugas deleted successfully"}
