from sqlalchemy import Column, String, Time, Date, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Jadwal(Base):
    __tablename__ = "jadwal"

    kd_jadwal = Column(String(length=10), primary_key=True, index=True)
    tanggal = Column(Date, nullable=False)
    waktu_mulai = Column(Time, nullable=False)
    waktu_selesai = Column(Time, nullable=False)
    kelas = Column(String(length=8), nullable=False)
    ruangan = Column(String(length=30), nullable=False)
    materi = Column(String(length=100), nullable=False)
    kd_matkul = Column(String(length=10), ForeignKey("matkul_prak.kd_matkul"))

    matkul_prak = relationship("MatkulPrak", back_populates="jadwal")
    kehadiran = relationship("Kehadiran", back_populates="jadwal", primaryjoin="Jadwal.kd_jadwal == Kehadiran.kd_jadwal")

