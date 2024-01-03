from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base

class MataKuliah(Base):
    __tablename__ = "mata_kuliah"

    kode_matkul = Column(String, primary_key=True, index=True)
    nama_matkul = Column(String)

    aslab = relationship("Aslab", back_populates="mata_kuliah")
    jadwal = relationship("Jadwal", back_populates="mata_kuliah")
    nilai_akhir = relationship("NilaiAkhir", back_populates="mata_kuliah")
    tugas = relationship("Tugas", back_populates="mata_kuliah")
