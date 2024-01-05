from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class NilaiAkhir(Base):
    __tablename__ = "nilai_akhir"

    praktikan_nim: str = Column(String, ForeignKey("praktikan.nim"), primary_key=True, index=True)
    mata_kuliah_kode_matkul: str = Column(String, ForeignKey("mata_kuliah.kode_matkul"), primary_key=True, index=True)
    nilai: int = Column(Integer)

    praktikan: str = relationship("Praktikan", back_populates="nilai_akhir")
    mata_kuliah: str = relationship("MataKuliah", back_populates="nilai_akhir")
