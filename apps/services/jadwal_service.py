from sqlalchemy.orm import Session
from apps.models.jadwal import Jadwal

def create_jadwal(db: Session, jadwal_data: Jadwal):
    db_jadwal = Jadwal(**jadwal_data.dict())
    db.add(db_jadwal)
    db.commit()
    db.refresh(db_jadwal)
    return db_jadwal

def get_jadwal(db: Session, kode_jadwal: str):
    return db.query(Jadwal).filter(Jadwal.kode_jadwal == kode_jadwal).first()

def get_jadwals(db: Session):
    return db.query(Jadwal).all()

def update_jadwal(db: Session, kode_jadwal: str, jadwal_data: Jadwal):
    db_jadwal = db.query(Jadwal).filter(Jadwal.kode_jadwal == kode_jadwal).first()
    for key, value in jadwal_data.dict().items():
        setattr(db_jadwal, key, value)
    db.commit()
    db.refresh(db_jadwal)
    return db_jadwal

def delete_jadwal(db: Session, kode_jadwal: str):
    db_jadwal = db.query(Jadwal).filter(Jadwal.kode_jadwal == kode_jadwal).first()
    db.delete(db_jadwal)
    db.commit()
    return {"message": "Jadwal deleted successfully"}
