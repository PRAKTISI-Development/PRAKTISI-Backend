# app/controllers/matkul_prak.py
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.matkul_prak import MatkulPrak as MatkulPrakModel

def create_matkul_prak(matkul_prak_data: MatkulPrakModel, db: Session = Depends(get_db)):
    db_matkul_prak = MatkulPrakModel(**matkul_prak_data)
    db.add(db_matkul_prak)
    db.commit()
    db.refresh(db_matkul_prak)
    return db_matkul_prak

def get_matkul_prak(kd_matkul: str, db: Session = Depends(get_db)):
    matkul_prak = db.query(MatkulPrakModel).filter(MatkulPrakModel.kd_matkul == kd_matkul).first()
    
    if matkul_prak is None:
        raise HTTPException(status_code=404, detail="Matkul Prak not found")
    
    return matkul_prak

def get_all_matkul_prak(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    matkul_prak_list = db.query(MatkulPrakModel).offset(skip).limit(limit).all()
    return matkul_prak_list

def update_matkul_prak(matkul_prak_data: MatkulPrakModel, kd_matkul: str, db: Session = Depends(get_db)):
    db_matkul_prak = db.query(MatkulPrakModel).filter(MatkulPrakModel.kd_matkul == kd_matkul).first()
    
    if db_matkul_prak is None:
        raise HTTPException(status_code=404, detail="Matkul Prak not found")
    
    for key, value in matkul_prak_data.dict().items():
        setattr(db_matkul_prak, key, value)
    
    db.commit()
    db.refresh(db_matkul_prak)
    return db_matkul_prak

def delete_matkul_prak(kd_matkul: str, db: Session = Depends(get_db)):
    db_matkul_prak = db.query(MatkulPrakModel).filter(MatkulPrakModel.kd_matkul == kd_matkul).first()
    
    if db_matkul_prak is None:
        raise HTTPException(status_code=404, detail="Matkul Prak not found")

    db.delete(db_matkul_prak)
    db.commit()
    return {"message": "Matkul Prak deleted successfully"}
