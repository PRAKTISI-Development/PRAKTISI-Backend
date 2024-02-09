from fastapi import HTTPException
from apps.models.tugas import Tugas
from apps.helpers.generator import identity_generator 
from apps.helpers.response import response

def create_tugas(request, tugas_data, db):
    try:
        tugas_data.kd_tugas = identity_generator()
        db_tugas = Tugas(**tugas_data.model_dump())

        db.add(db_tugas)
        db.commit()
        db.refresh(db_tugas)

        db_tugas.tanggal_dibuat = db_tugas.tanggal_dibuat.isoformat()
        db_tugas.tanggal_pengumpulan = db_tugas.tanggal_pengumpulan.isoformat()

        return response(request, status_code=201, success=True, msg="Successfully created", data=db_tugas)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_tugas(request, kd_tugas: str, db):
    try:
        tugas = db.query(Tugas).filter(Tugas.kd_tugas == kd_tugas)

        if tugas is None:
            raise HTTPException(status_code=404, detail="Tugas not found")
        
        return response(request,status_code=200, success=True, msg="Informasi ditemukan", data=tugas)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_all_tugas(request, db):
    try:
        tugas_list = db.query(Tugas).all()
        return response(request,status_code=200, success=True, msg="Tugas ditemukan", data=tugas_list)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def update_tugas(request, tugas_data: Tugas, kd_tugas: str, db):
    try:
        db_tugas = db.query(Tugas).filter(Tugas.kd_tugas == kd_tugas).first()
        if db_tugas is None:
            raise HTTPException(status_code=404, detail="Tugas not found")
        
        for key, value in tugas_data.dict().items():
            if key != "kd_tugas":
                setattr(db_tugas, key, value)
        db.commit()
        db.refresh(db_tugas)
        return response(request,status_code=200, success=True, msg="Berhasil memperbarui informasi", data=db_tugas)
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def delete_tugas(request, kd_tugas: str, db):
    try:
        db_tugas = db.query(Tugas).filter(Tugas.kd_tugas == kd_tugas).first()

        if db_tugas is None:
            raise HTTPException(status_code=404, detail="Tugas not found")

        db.delete(db_tugas)
        db.commit()

        return response(request,status_code=200, success=True, msg="Informasi berhasil dihapus", data=None)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)