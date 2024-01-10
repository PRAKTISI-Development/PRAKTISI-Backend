from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class NilaiAkhir(Base):
    __tablename__ = "nilai_akhir"

    praktikan_nim: str = Column(String(length=255), ForeignKey("praktikan.nim"), primary_key=True, index=True)
    mata_kuliah_kode_matkul: str = Column(String(length=255), ForeignKey("mata_kuliah.kode_matkul"), primary_key=True, index=True)
    nilai: int = Column(Integer)

    praktikan = relationship("Praktikan", back_populates="nilai_akhir")
    mata_kuliah = relationship("MataKuliah", back_populates="nilai_akhir")
