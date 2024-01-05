from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Tugas(Base):
    __tablename__ = "tugas"

    kode_tugas: str = Column(String, primary_key=True, index=True)
    nama_tugas: str = Column(String)
    deskripsi: str = Column(String)
    nilai: int = Column(Integer)
    mata_kuliah_kode_matkul: str = Column(String, ForeignKey("mata_kuliah.kode_matkul"))

    mata_kuliah: str = relationship("MataKuliah", back_populates="tugas")
