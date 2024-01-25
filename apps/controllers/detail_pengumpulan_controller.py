from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.detail_pengumpulan import DetailPengumpulan as DetailPengumpulanModel
from functools import lru_cache

def create_detail_pengumpulan(detail_pengumpulan_data: DetailPengumpulanModel, db: Session = Depends(get_db)):
    db_detail_pengumpulan = DetailPengumpulanModel(**detail_pengumpulan_data.dict())
    db.add(db_detail_pengumpulan)
    db.commit()
    db.flush()
    db.refresh(db_detail_pengumpulan)
    return db_detail_pengumpulan

@lru_cache
def get_detail_pengumpulan(usersid: str, kd_tugas: str, db: Session = Depends(get_db)):
    detail_pengumpulan = db.query(DetailPengumpulanModel).filter(
        DetailPengumpulanModel.usersid == usersid,
        DetailPengumpulanModel.kd_tugas == kd_tugas
    ).first()
    
    if detail_pengumpulan is None:
        raise HTTPException(status_code=404, detail="Detail Pengumpulan not found")
    
    return detail_pengumpulan

@lru_cache
def get_all_detail_pengumpulan(db: Session = Depends(get_db)):
    detail_pengumpulan_list = db.query(DetailPengumpulanModel).all()
    return detail_pengumpulan_list

def update_detail_pengumpulan(detail_pengumpulan_data: DetailPengumpulanModel, usersid: str, kd_tugas: str, db: Session = Depends(get_db)):
    db_detail_pengumpulan = db.query(DetailPengumpulanModel).filter(
        DetailPengumpulanModel.usersid == usersid,
        DetailPengumpulanModel.kd_tugas == kd_tugas
    ).first()
    
    if db_detail_pengumpulan is None:
        raise HTTPException(status_code=404, detail="Detail Pengumpulan not found")
    
    for key, value in detail_pengumpulan_data.dict().items():
        setattr(db_detail_pengumpulan, key, value)
    
    db.commit()
    db.refresh(db_detail_pengumpulan)
    return db_detail_pengumpulan

def delete_detail_pengumpulan(usersid: str, kd_tugas: str, db: Session = Depends(get_db)):
    db_detail_pengumpulan = db.query(DetailPengumpulanModel).filter(
        DetailPengumpulanModel.usersid == usersid,
        DetailPengumpulanModel.kd_tugas == kd_tugas
    ).first()
    
    if db_detail_pengumpulan is None:
        raise HTTPException(status_code=404, detail="Detail Pengumpulan not found")

    db.delete(db_detail_pengumpulan)
    db.commit()
    return {"message": "Detail Pengumpulan deleted successfully"}
