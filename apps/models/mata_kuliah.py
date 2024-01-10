from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from apps.database import Base

class MataKuliah(Base):
    __tablename__ = "mata_kuliah"

    kode_matkul: str = Column(String(length=255), primary_key=True, index=True)
    nama_matkul: str = Column(String(length=255))

    aslab = relationship("Aslab", back_populates="mata_kuliah")
    jadwal = relationship("Jadwal", back_populates="mata_kuliah")
    nilai_akhir = relationship("NilaiAkhir", back_populates="mata_kuliah")
    tugas = relationship("Tugas", back_populates="mata_kuliah")
