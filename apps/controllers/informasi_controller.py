from fastapi import HTTPException
from apps.models.informasi import Informasi as InformasiModel
from apps.helpers.generator import identity_generator
from apps.helpers.response import response

def create_informasi(request, informasi_data, db):
    try:
        # Generate ID
        informasi_data.kd_informasi = identity_generator()

        db_informasi = InformasiModel(**informasi_data.dict())
        db.add(db_informasi)
        db.commit()
        db.refresh(db_informasi)

        # Adjustments for response
        db_informasi.tanggal = db_informasi.tanggal.isoformat()

        return response(request, status_code=201, success=True, msg="Successfully created", data=db_informasi)

    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_informasi(request,kd_informasi: str, db):
    try:
        informasi = db.query(InformasiModel).filter(InformasiModel.kd_informasi == kd_informasi).first()

        if informasi is None:
            raise HTTPException(status_code=404, detail="Informasi not found")
        
        return response(request,status_code=200, success=True, msg="Informasi ditemukan", data=informasi)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_all_informasi(request,db):
    try:
        informasi_list = db.query(InformasiModel).all()
        return response(request,status_code=200, success=True, msg="Informasi ditemukan", data=informasi_list)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def update_informasi(request,informasi_data: InformasiModel, kd_informasi: str, db):
    try:
        db_informasi = db.query(InformasiModel).filter(InformasiModel.kd_informasi == kd_informasi).first() 

        if db_informasi is None:
            raise HTTPException(status_code=404, detail="Informasi not found")
        
        for key, value in informasi_data.dict().items():
            setattr(db_informasi, key, value)
        
        db.commit()
        db.refresh(db_informasi)
        return response(request,status_code=200, success=True, msg="Berhasil memperbarui informasi", data=db_informasi)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def delete_informasi(request,kd_informasi: str, db):
    try:
        db_informasi = db.query(InformasiModel).filter(InformasiModel.kd_informasi == kd_informasi).first()
        
        if db_informasi is None:
            raise HTTPException(status_code=404, detail="Informasi not found")

        db.delete(db_informasi)
        db.commit()

        return response(request,status_code=200, success=True, msg="Informasi berhasil dihapus", data=None)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)