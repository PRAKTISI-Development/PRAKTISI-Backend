from typing import ClassVar
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from apps.database import Base
from pydantic import BaseModel

class MataKuliah(BaseModel):
    __tablename__ = "mata_kuliah"

    kode_matkul: str = Column(String, primary_key=True, index=True)
    nama_matkul: str = Column(String)

    aslab: str = relationship("Aslab", back_populates="mata_kuliah")
    jadwal = relationship("Jadwal", back_populates="mata_kuliah")
    nilai_akhir: int = relationship("NilaiAkhir", back_populates="mata_kuliah")
    tugas: str = relationship("Tugas", back_populates="mata_kuliah")
