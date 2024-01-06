from sqlalchemy.orm import Session
from apps.models.mata_kuliah import MataKuliah

def get_mata_kuliah(db: Session):
    return db.query(MataKuliah).all()

def get_mata_kuliah_by_code(db: Session, kode_matkul: str):
    return db.query(MataKuliah).filter(MataKuliah.kode_matkul == kode_matkul).first()

def create_mata_kuliah(db: Session, mata_kuliah_data: dict):
    db_mata_kuliah = MataKuliah(**mata_kuliah_data)
    db.add(db_mata_kuliah)
    db.commit()
    db.refresh(db_mata_kuliah)
    return db_mata_kuliah

def update_mata_kuliah(db: Session, kode_matkul: str, mata_kuliah_data: dict):
    db_mata_kuliah = db.query(MataKuliah).filter(MataKuliah.kode_matkul == kode_matkul).first()
    for key, value in mata_kuliah_data.items():
        setattr(db_mata_kuliah, key, value)
    db.commit()
    db.refresh(db_mata_kuliah)
    return db_mata_kuliah

def delete_mata_kuliah(db: Session, kode_matkul: str):
    db_mata_kuliah = db.query(MataKuliah).filter(MataKuliah.kode_matkul == kode_matkul).first()
    db.delete(db_mata_kuliah)
    db.commit()
    return {"message": "Mata Kuliah deleted successfully"}
