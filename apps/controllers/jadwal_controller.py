from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.jadwal import Jadwal 

def create_jadwal(jadwal_data: Jadwal, db: Session = Depends(get_db)):
    db_jadwal = Jadwal(**jadwal_data)
    db.add(db_jadwal)
    db.commit()
    db.refresh(db_jadwal)
    return db_jadwal

def get_jadwal(kd_jadwal: str, db: Session = Depends(get_db)):
    jadwal = db.query(Jadwal).filter(Jadwal.kd_jadwal == kd_jadwal).first()
    if jadwal is None:
        raise HTTPException(status_code=404, detail="Jadwal not found")
    return jadwal

def get_all_jadwal(db: Session = Depends(get_db)):
    jadwals = db.query(Jadwal).all()
    return jadwals

def update_jadwal(jadwal_data: Jadwal, kd_jadwal: str, db: Session = Depends(get_db)):
    db_jadwal = db.query(Jadwal).filter(Jadwal.kd_jadwal == kd_jadwal).first()
    if db_jadwal is None:
        raise HTTPException(status_code=404, detail="Jadwal not found")
    
    for key, value in jadwal_data.dict().items():
        setattr(db_jadwal, key, value)
    db.commit()
    db.refresh(db_jadwal)
    return db_jadwal

def delete_jadwal(kd_jadwal: str, db: Session = Depends(get_db)):
    db_jadwal = db.query(Jadwal).filter(Jadwal.kd_jadwal == kd_jadwal).first()
    if db_jadwal is None:
        raise HTTPException(status_code=404, detail="Jadwal not found")

    db.delete(db_jadwal)
    db.commit()
    return {"message": "Jadwal deleted successfully"}
