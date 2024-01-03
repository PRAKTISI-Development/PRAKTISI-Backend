from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class NilaiAkhir(Base):
    __tablename__ = "nilai_akhir"

    praktikan_nim = Column(String, ForeignKey("praktikan.nim"), primary_key=True, index=True)
    mata_kuliah_kode_matkul = Column(String, ForeignKey("mata_kuliah.kode_matkul"), primary_key=True, index=True)
    nilai = Column(Integer)

    praktikan = relationship("Praktikan", back_populates="nilai_akhir")
    mata_kuliah = relationship("MataKuliah", back_populates="nilai_akhir")
