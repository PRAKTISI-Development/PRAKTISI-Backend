from fastapi import HTTPException
from apps.models.jadwal import Jadwal 
from apps.helpers.generator import identity_generator
from apps.helpers.response import response

def create_jadwal(request, jadwal_data, db):
        try:
            # Generate ID
            jadwal_data.kd_jadwal = identity_generator()

            db_jadwal = Jadwal(**jadwal_data.dict())
            db.add(db_jadwal)
            db.commit()
            db.refresh(db_jadwal)

            # Adjustments for response
            db_jadwal.tanggal = db_jadwal.tanggal.isoformat()
            db_jadwal.waktu_mulai = db_jadwal.waktu_mulai.strftime("%H-%M-%S")
            db_jadwal.waktu_selesai = db_jadwal.waktu_selesai.strftime("%H-%M-%S")
            
            return response(request, status_code=201, success=True, msg="Successfully created", data=db_jadwal)

        except HTTPException as e:
            return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_jadwal(request, kd_jadwal: str, db):
    try:
        jadwal = db.query(Jadwal).filter(Jadwal.kd_jadwal == kd_jadwal).first()
         
        if jadwal is None:
            raise HTTPException(status_code=404, detail="Jadwal not found")
        
        return response(request,status_code=200, success=True, msg="Jadwal ditemukan", data=jadwal)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_all_jadwal(request, db):
    try:
        jadwals = db.query(Jadwal).all()
        return response(request,status_code=200, success=True, msg="Jadwal ditemukan", data=jadwals)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def update_jadwal(request, jadwal_data: Jadwal, kd_jadwal: str, db):
    try :
        db_jadwal = db.query(Jadwal).filter(Jadwal.kd_jadwal == kd_jadwal).first()

        if db_jadwal is None:
            raise HTTPException(status_code=404, detail="Jadwal not found")
        
        for key, value in jadwal_data.dict().items():
            setattr(db_jadwal, key, value)

        db.commit()
        db.refresh(db_jadwal)
        return response(request,status_code=200, success=True, msg="Berhasil memperbarui jadwal", data=db_jadwal)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def delete_jadwal(request, kd_jadwal: str, db):
    try :
        db_jadwal = db.query(Jadwal).filter(Jadwal.kd_jadwal == kd_jadwal).first()

        if db_jadwal is None:
            raise HTTPException(status_code=404, detail="Jadwal not found")

        db.delete(db_jadwal)
        db.commit()

        return response(request,status_code=200, success=True, msg="Jadwal berhasil dihapus", data=None)        
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)