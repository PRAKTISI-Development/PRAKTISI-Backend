from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base
from pydantic import BaseModel

class MataKuliah(Base):
    __tablename__ = "mata_kuliah"

    kode_matkul: str = Column(String, primary_key=True, index=True)
    nama_matkul: str = Column(String)

    aslab = relationship("Aslab", back_populates="mata_kuliah")
    jadwal = relationship("Jadwal", back_populates="mata_kuliah")
    nilai_akhir = relationship("NilaiAkhir", back_populates="mata_kuliah")
    tugas = relationship("Tugas", back_populates="mata_kuliah")

class MataKuliahPydantic(BaseModel):
    kode_matkul: str
    nama_matkul: str

    class Config:
        orm_mode = True
