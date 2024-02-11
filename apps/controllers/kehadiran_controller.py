from fastapi import HTTPException
from fastapi.responses import JSONResponse
from apps.models.kehadiran import Kehadiran as KehadiranModel
from apps.helpers.response import response
from sqlalchemy.orm import joinedload, subqueryload, undefer
from apps.models.jadwal import Jadwal as JadwalModel

def create_kehadiran(request, kehadiran_data, db):
    try:
        db_kehadiran = KehadiranModel(**kehadiran_data.model_dump())
        db.add(db_kehadiran)
        db.commit()
        db.refresh(db_kehadiran)
        return response(request, status_code=201, success=True, msg="Successfully created", data=db_kehadiran)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_kehadiran(request, usersid, kd_jadwal, db):
    try:
        
        kehadiran = db.query(KehadiranModel).filter(
            KehadiranModel.usersid == usersid,
            KehadiranModel.kd_jadwal == kd_jadwal,
        ).first()
        
        if kehadiran is None:
            raise HTTPException(status_code=404, detail="Kehadiran not found")
        
        return response(request, status_code=200, success=True, msg="Kehadiran ditemukan", data=kehadiran)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

# def get_all_kehadiran(request, db):
#     try:
#         kehadiran_list = db.query(KehadiranModel).all()
#         kehadiran_list = (
#             db.query(KehadiranModel)
#             .options(joinedload(KehadiranModel.jadwal).joinedload(JadwalModel.matkul_prak)) # Memuat data Jadwal bersamaan dengan Kehadiran
#             .all()
#         )
#         return response(request, status_code=200, success=True, msg="Kehadiran ditemukan", data=kehadiran_list)
    
#     except HTTPException as e:
#         return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)
def get_all_kehadiran(request, db):
    try:
        # kehadiran_list = (
        #     db.query(KehadiranModel)
        #     .join(JadwalModel, KehadiranModel.kd_jadwal == JadwalModel.kd_jadwal)
        #     .with_entities(KehadiranModel, JadwalModel.kd_jadwal)
        #     .all()
        # )
        kehadiran_list = (
            db.query(KehadiranModel)
            .options(subqueryload(KehadiranModel.jadwal).undefer(JadwalModel.kd_matkul))
            .all()
        )
        print(kehadiran_list)
        # print(KehadiranModel(**dict(kehadiran_list).model_dump()))
        return response(request, status_code=200, success=True, msg="Kehadiran ditemukan", data=kehadiran_list)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)


def update_kehadiran(request, kehadiran_data, usersid, kd_jadwal, db):
    try:
        db_kehadiran = db.query(KehadiranModel).filter(
            KehadiranModel.usersid == usersid,
            KehadiranModel.kd_jadwal == kd_jadwal
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

def delete_kehadiran(request, usersid, kd_jadwal, db):
    try:
        db_kehadiran = db.query(KehadiranModel).filter(
            KehadiranModel.usersid == usersid,
            KehadiranModel.kd_jadwal == kd_jadwal
        ).first()
        
        if db_kehadiran is None:
            raise HTTPException(status_code=404, detail="Kehadiran not found")
        
        db.delete(db_kehadiran)
        db.commit()
        return response(request, status_code=200, success=True, msg="Kehadiran berhasil dihapus", data=None)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)