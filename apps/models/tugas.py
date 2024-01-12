from datetime import datetime
from sqlalchemy import Column, String, Enum, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Tugas(Base):
    __tablename__ = "tugas"

    kd_tugas: str = Column(String(length=10), primary_key=True, index=True)
    jenis_tugas: str = Column(Enum('Post Test', 'Proyek Akhir'), nullable=False)
    nama_tugas: str = Column(String(length=100), nullable=False)
    deskripsi_tugas: str = Column(Text, nullable=False)
    tanggal_dibuat: datetime = Column(DateTime, nullable=False)
    tanggal_pengumpulan: datetime = Column(DateTime, nullable=False)
    kd_matkul: str = Column(String(length=10), ForeignKey("matkul_prak.kd_matkul"))

    matkul_prak = relationship("MatkulPrak", back_populates="tugas")
    detail_pengumpulan = relationship("DetailPengumpulan", back_populates="tugas")
