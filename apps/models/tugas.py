from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Tugas(Base):
    __tablename__ = 'tugas'

    kd_tugas = Column(String(length=10), primary_key=True)
    jenis_tugas = Column(Enum('Post Test', 'Proyek Akhir'), nullable=False)
    nama_tugas = Column(String(length=100), nullable=False)
    deskripsi_tugas = Column(String(length=100), nullable=False)
    tanggal_dibuat = Column(DateTime, nullable=False)
    tanggal_pengumpulan = Column(DateTime, nullable=False)
    kd_matkul = Column(String(length=10), ForeignKey('matkul_prak.kd_matkul'))

    user = relationship('MatkulPrak', back_populates='tugas')
    matkul_prak = relationship('MatkulPrak', back_populates='tugas')  
    detail_pengumpulan = relationship('DetailPengumpulan', back_populates='tugas')
