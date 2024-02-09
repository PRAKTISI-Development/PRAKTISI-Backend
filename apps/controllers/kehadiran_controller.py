from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.kehadiran import Kehadiran as KehadiranModel
from apps.schemas.kehadiran_schema import KehadiranSchema
from apps.helpers.response import response

def create_kehadiran(request: Request, kehadiran_data: KehadiranSchema, db: Session = Depends(get_db)):
    try:
        db_kehadiran = KehadiranModel(**kehadiran_data.model_dump())
        db.add(db_kehadiran)
        db.commit()
        db.refresh(db_kehadiran)
        return response(request, status_code=201, success=True, msg="Successfully created", data=db_kehadiran)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_kehadiran(request: Request, usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    try:
        kehadiran = db.query(KehadiranModel).filter(
            KehadiranModel.usersid == usersid,
            KehadiranModel.kd_matkul == kd_matkul,
            KehadiranModel.pertemuan == pertemuan
        ).first()
        
        if kehadiran is None:
            raise HTTPException(status_code=404, detail="Kehadiran not found")
        
        return response(request, status_code=200, success=True, msg="Kehadiran ditemukan", data=kehadiran)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_all_kehadiran(request: Request, db: Session = Depends(get_db)):
    try:
        kehadiran_list = db.query(KehadiranModel).all()
        return response(request, status_code=200, success=True, msg="Kehadiran ditemukan", data=kehadiran_list)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def update_kehadiran(request: Request, kehadiran_data: KehadiranSchema, usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    try:
        db_kehadiran = db.query(KehadiranModel).filter(
            KehadiranModel.usersid == usersid,
            KehadiranModel.kd_matkul == kd_matkul,
            KehadiranModel.pertemuan == pertemuan
        ).first()
        
        if db_kehadiran is None:
            raise HTTPException(status_code=404, detail="Kehadiran not found")
        
        for key, value in kehadiran_data.model_dump().items():
            setattr(db_kehadiran, key, value)
        
        db.commit()
        db.refresh(db_kehadiran)
        return response(request, status_code=200, success=True, msg="Berhasil memperbarui kehadiran", data=db_kehadiran)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def delete_kehadiran(request: Request, usersid: str, kd_matkul: str, pertemuan: int, db: Session = Depends(get_db)):
    try:
        db_kehadiran = db.query(KehadiranModel).filter(
            KehadiranModel.usersid == usersid,
            KehadiranModel.kd_matkul == kd_matkul,
            KehadiranModel.pertemuan == pertemuan
        ).first()
        
        if db_kehadiran is None:
            raise HTTPException(status_code=404, detail="Kehadiran not found")
        
        db.delete(db_kehadiran)
        db.commit()
        return response(request, status_code=200, success=True, msg="Kehadiran berhasil dihapus", data=None)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)
