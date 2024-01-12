from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Kehadiran(Base):
    __tablename__ = "kehadiran"

    usersid: str = Column(String(length=20), ForeignKey("users.userid"), primary_key=True, index=True)
    kd_matkul: str = Column(String(length=10), ForeignKey("matkul_prak.kd_matkul"), primary_key=True, index=True)
    pertemuan: int = Column(Integer, nullable=False)
    materi: str = Column(String(length=100), nullable=False)
    tanggal: datetime = Column(DateTime, nullable=False)
    keterangan: str = Column(Enum('Hadir', 'Tidak Hadir', '', ''), nullable=False)

    user = relationship("User", back_populates="kehadiran")
    matkul_prak = relationship("MatkulPrak", back_populates="kehadiran")
