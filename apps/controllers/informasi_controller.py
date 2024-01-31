from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models.informasi import Informasi as InformasiModel
from apps.schemas.informasi_schema import InformasiSchema
from apps.helpers.generator import identity_generator_information
from apps.helpers.response import post_response,response
from sqlalchemy.orm import attributes

def create_informasi(informasi_data: InformasiSchema, db: Session = Depends(get_db)):
    try:
        # Generate ID
        informasi_data.kd_informasi = identity_generator_information()

        db_informasi = InformasiModel(**informasi_data.model_dump())
        db.add(db_informasi)
        db.commit()
        db.refresh(db_informasi)

        # Adjustments for response
        db_informasi.tanggal = db_informasi.tanggal.isoformat()
        instance_dict = attributes.instance_dict(db_informasi)
        instance_dict.pop('_sa_instance_state', None)

        return post_response(status_code=200, success=True, msg="Successfully created", data=instance_dict)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error occurred")


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
