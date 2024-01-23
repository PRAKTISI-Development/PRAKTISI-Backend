from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.informasi import Informasi as InformasiModel
from apps.schemas.informasi_schema import InformasiSchema

def create_informasi(informasi_data: InformasiSchema, db: Session = Depends(get_db)):
    try:

        db_informasi = InformasiModel(**informasi_data.dict())

        db.add(db_informasi)
        db.commit()
        db.refresh(db_informasi)

        print(db_informasi)

        return db_informasi
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=e.detail)


def get_informasi(kd_informasi: str, db: Session = Depends(get_db)):
    informasi = db.query(InformasiModel).filter(InformasiModel.kd_informasi == kd_informasi).first()
    
    if informasi is None:
        raise HTTPException(status_code=404, detail="Informasi not found")
    
    return informasi

def get_all_informasi(db: Session = Depends(get_db)):
    informasi_list = db.query(InformasiModel).all()
    return informasi_list

def update_informasi(informasi_data: InformasiModel, kd_informasi: str, db: Session = Depends(get_db)):
    db_informasi = db.query(InformasiModel).filter(InformasiModel.kd_informasi == kd_informasi).first()
    
    if db_informasi is None:
        raise HTTPException(status_code=404, detail="Informasi not found")
    
    for key, value in informasi_data.dict().items():
        setattr(db_informasi, key, value)
    
    db.commit()
    db.refresh(db_informasi)
    return db_informasi

def delete_informasi(kd_informasi: str, db: Session = Depends(get_db)):
    db_informasi = db.query(InformasiModel).filter(InformasiModel.kd_informasi == kd_informasi).first()
    
    if db_informasi is None:
        raise HTTPException(status_code=404, detail="Informasi not found")

    db.delete(db_informasi)
    db.commit()
    return {"message": "Informasi deleted successfully"}
