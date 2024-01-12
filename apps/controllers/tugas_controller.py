from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.tugas import Tugas 

def create_tugas(tugas_data: Tugas, db: Session = Depends(get_db)):
    db_tugas = Tugas(**tugas_data)
    db.add(db_tugas)
    db.commit()
    db.refresh(db_tugas)
    return db_tugas

def get_tugas(kd_tugas: str, db: Session = Depends(get_db)):
    tugas = db.query(Tugas).filter(Tugas.kd_tugas == kd_tugas).first()
    if tugas is None:
        raise HTTPException(status_code=404, detail="Tugas not found")
    return tugas

def get_all_tugas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tugas_list = db.query(Tugas).offset(skip).limit(limit).all()
    return tugas_list

def update_tugas(tugas_data: Tugas, kd_tugas: str, db: Session = Depends(get_db)):
    db_tugas = db.query(Tugas).filter(Tugas.kd_tugas == kd_tugas).first()
    if db_tugas is None:
        raise HTTPException(status_code=404, detail="Tugas not found")
    
    for key, value in tugas_data.dict().items():
        setattr(db_tugas, key, value)
    db.commit()
    db.refresh(db_tugas)
    return db_tugas

def delete_tugas(kd_tugas: str, db: Session = Depends(get_db)):
    db_tugas = db.query(Tugas).filter(Tugas.kd_tugas == kd_tugas).first()
    if db_tugas is None:
        raise HTTPException(status_code=404, detail="Tugas not found")

    db.delete(db_tugas)
    db.commit()
    return {"message": "Tugas deleted successfully"}
