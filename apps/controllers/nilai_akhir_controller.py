from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from apps.database import get_db
from apps.models.nilai_akhir import NilaiAkhir as NilaiAkhirModel
from apps.schemas.nilai_akhir_schema import NilaiAkhirSchema
from apps.schemas.akumulasi_schema import *
import pandas as pd

def create_nilai_akhir(nilai_akhir_data: NilaiAkhirSchema, db: Session = Depends(get_db)):
    db_nilai_akhir = NilaiAkhirModel(**nilai_akhir_data.model_dump())
    db.add(db_nilai_akhir)
    db.commit()
    db.refresh(db_nilai_akhir)
    return db_nilai_akhir


# on progress
def get_akumulasi(kd_matkul:str,db:Session=Depends(get_db)):
    try:
        params = kd_matkul
        query = text(f"call akumulasi_nilai_dan_kehadiran('{params}')")
        result = db.execute(query)
        save_excel(result)

    except Exception as e:
        print(e)

def save_excel(result):
    try:
        df = pd.DataFrame(result.fetchall(),columns=result.keys())
        # Simpan DataFrame ke file Excel
        excel_filename = 'hasil_query.xlsx'
        df.to_excel(excel_filename, index=False)

        print(f"DataFrame telah disimpan ke file Excel: {excel_filename}")

    except Exception as e:
        print(e)
# end progress



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