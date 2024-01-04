from sqlalchemy.orm import Session
from apps.models import NilaiAkhir

def create_nilai_akhir(db: Session, nilai_akhir_data: NilaiAkhir):
    db_nilai_akhir = NilaiAkhir(**nilai_akhir_data.dict())
    db.add(db_nilai_akhir)
    db.commit()
    db.refresh(db_nilai_akhir)
    return db_nilai_akhir

def get_nilai_akhir(db: Session, praktikan_nim: str, mata_kuliah_kode_matkul: str):
    return db.query(NilaiAkhir).filter(
        NilaiAkhir.praktikan_nim == praktikan_nim,
        NilaiAkhir.mata_kuliah_kode_matkul == mata_kuliah_kode_matkul
    ).first()

def get_nilai_akhirs(db: Session):
    return db.query(NilaiAkhir).all()

def update_nilai_akhir(db: Session, praktikan_nim: str, mata_kuliah_kode_matkul: str, nilai_akhir_data: NilaiAkhirCreate):
    db_nilai_akhir = db.query(NilaiAkhir).filter(
        NilaiAkhir.praktikan_nim == praktikan_nim,
        NilaiAkhir.mata_kuliah_kode_matkul == mata_kuliah_kode_matkul
    ).first()
    for key, value in nilai_akhir_data.dict().items():
        setattr(db_nilai_akhir, key, value)
    db.commit()
    db.refresh(db_nilai_akhir)
    return db_nilai_akhir

def delete_nilai_akhir(db: Session, praktikan_nim: str, mata_kuliah_kode_matkul: str):
    db_nilai_akhir = db.query(NilaiAkhir).filter(
        NilaiAkhir.praktikan_nim == praktikan_nim,
        NilaiAkhir.mata_kuliah_kode_matkul == mata_kuliah_kode_matkul
    ).first()
    db.delete(db_nilai_akhir)
    db.commit()
    return {"message": "Nilai Akhir deleted successfully"}
