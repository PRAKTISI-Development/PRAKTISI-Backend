from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Tugas(Base):
    __tablename__ = "tugas"

    kode_tugas: str = Column(String(length=10), primary_key=True, index=True)
    nama_tugas: str = Column(String(length=255))
    deskripsi: str = Column(String(length=255))
    nilai: int = Column(Integer)
    mata_kuliah_kode_matkul: str = Column(String(length=255), ForeignKey("mata_kuliah.kode_matkul"))

    mata_kuliah = relationship("MataKuliah", back_populates="tugas")
