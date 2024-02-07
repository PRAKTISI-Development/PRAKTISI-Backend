from fastapi import HTTPException, Form
from apps.models.detail_pengumpulan import DetailPengumpulan as DetailPengumpulanModel
from functools import lru_cache
from apps.helpers.response import response
import os
from fastapi import UploadFile
from apps.middleware.validation import file_validation

def create_detail_pengumpulan(request, detail_pengumpulan_data, db):
    try:
        model_dump_dict = detail_pengumpulan_data.model_dump()

        model_dict = {key: value for key, value in model_dump_dict.items() if key != 'file'}

        if detail_pengumpulan_data.file:
            file_validation(detail_pengumpulan_data.file)
            file_paths = save_uploaded_file(detail_pengumpulan_data.file)
            model_dict['file_path'] = file_paths

        db_detail_pengumpulan = DetailPengumpulanModel(**model_dict)

        db.add(db_detail_pengumpulan)
        db.commit()
        db.refresh(db_detail_pengumpulan)

        db_detail_pengumpulan.tanggal_dikumpul = db_detail_pengumpulan.tanggal_dikumpul.isoformat()
        db_detail_pengumpulan.file_path = file_paths if file_paths else None

        return response(request, status_code=201, success=True, msg="Successfully created", data=db_detail_pengumpulan)

    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def save_uploaded_file(file: UploadFile):
    upload_folder = "uploads"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path

    
@lru_cache
def get_detail_pengumpulan(request, usersid: str, kd_tugas: str, db):
    try:
        detail_pengumpulan = db.query(DetailPengumpulanModel).filter(
            DetailPengumpulanModel.usersid == usersid,
            DetailPengumpulanModel.kd_tugas == kd_tugas
        ).first()
        
        if detail_pengumpulan is None:
            raise HTTPException(status_code=404, detail="Detail Pengumpulan not found")
        
        return response(request,status_code=200, success=True, msg="Data ditemukan", data=detail_pengumpulan)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

@lru_cache
def get_all_detail_pengumpulan(request, db):
    try: 
        detail_pengumpulan_list = db.query(DetailPengumpulanModel).all()
        return response(request,status_code=200, success=True, msg="Informasi ditemukan", data=detail_pengumpulan_list)
    
    except HTTPException as  e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)
    
def update_detail_pengumpulan(request, detail_pengumpulan_data: DetailPengumpulanModel, usersid: str, kd_tugas: str, db):
    try:
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
        return response(request,status_code=200, success=True, msg="Berhasil memperbarui data", data=db_detail_pengumpulan)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)
    
def delete_detail_pengumpulan(request, usersid: str, kd_tugas: str, db):
    try:
        db_detail_pengumpulan = db.query(DetailPengumpulanModel).filter(
            DetailPengumpulanModel.usersid == usersid,
            DetailPengumpulanModel.kd_tugas == kd_tugas
        ).first()
        
        if db_detail_pengumpulan is None:
            raise HTTPException(status_code=404, detail="Detail Pengumpulan not found")

        db.delete(db_detail_pengumpulan)
        db.commit()
        return response(request,status_code=200, success=True, msg="Data berhasil dihapus", data=None)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)