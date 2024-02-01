from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.kehadiran import Kehadiran as KehadiranModel
from apps.schemas.kehadiran_schema import KehadiranSchema
from sqlalchemy.orm import attributes

def create_kehadiran(request, kehadiran_data: KehadiranSchema, db: Session = Depends(get_db)):
    db_kehadiran = KehadiranModel(**kehadiran_data.model_dump())
    print(db_kehadiran)
    db.add(db_kehadiran)
    db.commit()
    db.refresh(db_kehadiran)

    # instance_dict = attributes.instance_dict(db_kehadiran)
    # instance_dict.pop('_sa_instance_state', None)
    return db_kehadiran

def get_kehadiran(request: Request, usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    kehadiran = db.query(KehadiranModel).filter(
        KehadiranModel.usersid == usersid,
        # KehadiranModel.matkul_prak_kd_matkul == kd_matkul,
        KehadiranModel.pertemuan == pertemuan
    ).first()
    
    if kehadiran is None:
        raise HTTPException(status_code=404, detail="Kehadiran not found")
    
    return kehadiran

def get_all_kehadiran(db: Session = Depends(get_db)):
    kehadiran_list = db.query(KehadiranModel).all()
    return kehadiran_list

def update_kehadiran(kehadiran_data: KehadiranModel, usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    db_kehadiran = db.query(KehadiranModel).filter(
        KehadiranModel.usersid == usersid,
        # KehadiranModel.matkul_prak_kd_matkul == kd_matkul,
        KehadiranModel.pertemuan == pertemuan
    ).first()
    
    if db_kehadiran is None:
        raise HTTPException(status_code=404, detail="Kehadiran not found")
    
    for key, value in kehadiran_data.dict().items():
        setattr(db_kehadiran, key, value)
    
    db.commit()
    db.refresh(db_kehadiran)
    return db_kehadiran

def delete_kehadiran(usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    db_kehadiran = db.query(KehadiranModel).filter(
        KehadiranModel.usersid == usersid,
        # KehadiranModel.kd_matkul == kd_matkul,
        KehadiranModel.pertemuan == pertemuan
    ).first()
    
    if db_kehadiran is None:
        raise HTTPException(status_code=404, detail="Kehadiran not found")

    db.delete(db_kehadiran)
    db.commit()
    return {"message": "Kehadiran deleted successfully"}
