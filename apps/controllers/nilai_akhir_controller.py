from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.nilai_akhir import NilaiAkhir as NilaiAkhirModel

def create_nilai_akhir(nilai_akhir_data: NilaiAkhirModel, db: Session = Depends(get_db)):
    db_nilai_akhir = NilaiAkhirModel(**nilai_akhir_data)
    db.add(db_nilai_akhir)
    db.commit()
    db.refresh(db_nilai_akhir)
    return db_nilai_akhir

def get_nilai_akhir(usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    nilai_akhir = db.query(NilaiAkhirModel).filter(
        NilaiAkhirModel.usersid == usersid,
        NilaiAkhirModel.kd_matkul == kd_matkul
    ).first()
    
    if nilai_akhir is None:
        raise HTTPException(status_code=404, detail="Nilai Akhir not found")
    
    return nilai_akhir

def get_all_nilai_akhir(db: Session = Depends(get_db)):
    nilai_akhir_list = db.query(NilaiAkhirModel).all()
    return nilai_akhir_list

def update_nilai_akhir(nilai_akhir_data: NilaiAkhirModel, usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    db_nilai_akhir = db.query(NilaiAkhirModel).filter(
        NilaiAkhirModel.usersid == usersid,
        NilaiAkhirModel.kd_matkul == kd_matkul
    ).first()
    
    if db_nilai_akhir is None:
        raise HTTPException(status_code=404, detail="Nilai Akhir not found")
    
    for key, value in nilai_akhir_data.dict().items():
        setattr(db_nilai_akhir, key, value)
    
    db.commit()
    db.refresh(db_nilai_akhir)
    return db_nilai_akhir

def delete_nilai_akhir(usersid: str, kd_matkul: str, db: Session = Depends(get_db)):
    db_nilai_akhir = db.query(NilaiAkhirModel).filter(
        NilaiAkhirModel.usersid == usersid,
        NilaiAkhirModel.kd_matkul == kd_matkul
    ).first()
    
    if db_nilai_akhir is None:
        raise HTTPException(status_code=404, detail="Nilai Akhir not found")

    db.delete(db_nilai_akhir)
    db.commit()