from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Tugas(Base):
    __tablename__ = "tugas"

    kode_tugas = Column(String, primary_key=True, index=True)
    nama_tugas = Column(String)
    deskripsi = Column(String)
    nilai = Column(Integer)
    mata_kuliah_kode_matkul = Column(String, ForeignKey("mata_kuliah.kode_matkul"))

    mata_kuliah = relationship("MataKuliah", back_populates="tugas")
