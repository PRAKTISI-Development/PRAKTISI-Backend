from fastapi import HTTPException
from apps.models.matkul_prak import MatkulPrak as MatkulPrakModel
from apps.helpers.response import response

def create_matkul_prak(request, matkul_prak_data, db):
    try:
        db_matkul_prak = MatkulPrakModel(**matkul_prak_data.model_dump())

        db.add(db_matkul_prak)
        db.commit()
        db.refresh(db_matkul_prak)

        return response(request, status_code=201, success=True,msg="Successfully Created", data=db_matkul_prak)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_matkul_prak(request, kd_matkul: str, db):
    try:
        matkul_prak = db.query(MatkulPrakModel).filter(MatkulPrakModel.kd_matkul == kd_matkul).first()
        
        if matkul_prak is None:
            raise HTTPException(status_code=404, detail="Matkul Prak not found")
        
        return response(request,status_code=200, success=True, msg="Matkul ditemukan", data=matkul_prak)
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def get_all_matkul_prak(request, db):
    try :
        matkul_prak_list = db.query(MatkulPrakModel).all()

        return response(request,status_code=200, success=True, msg="Matkul ditemukan", data=matkul_prak_list)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)    

def update_matkul_prak(request, matkul_prak_data: MatkulPrakModel, kd_matkul: str, db):
    try :
        db_matkul_prak = db.query(MatkulPrakModel).filter(MatkulPrakModel.kd_matkul == kd_matkul).first()
        
        if db_matkul_prak is None:
            raise HTTPException(status_code=404, detail="Matkul Prak not found")
        
        for key, value in matkul_prak_data.dict().items():
            if key != "kd_matkul":
                setattr(db_matkul_prak, key, value)
        
        db.commit()
        db.refresh(db_matkul_prak)
        return response(request,status_code=200, success=True, msg="Berhasil memperbarui Jadwal", data=db_matkul_prak)
    
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)

def delete_matkul_prak(request, kd_matkul: str, db):
    try:
        db_matkul_prak = db.query(MatkulPrakModel).filter(MatkulPrakModel.kd_matkul == kd_matkul).first()
        
        if db_matkul_prak is None:
            raise HTTPException(status_code=404, detail="Matkul Prak not found")

        db.delete(db_matkul_prak)
        db.commit()
        return response(request,status_code=200, success=True, msg="Matkul berhasil dihapus", data=None)
    except HTTPException as e:
        return response(request, status_code=e.status_code, success=False, msg=e.detail, data=None)