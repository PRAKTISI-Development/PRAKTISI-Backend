from datetime import date, time
from sqlalchemy import Column, Date, Time, String, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Jadwal(Base):
    __tablename__ = "jadwal"

    kd_jadwal: str = Column(String(length=10), primary_key=True, index=True)
    tanggal: date = Column(Date, nullable=False)
    waktu_mulai: time = Column(Time, nullable=False)
    waktu_selesai: time = Column(Time, nullable=False)
    ruangan: str = Column(String(length=30), nullable=False)
    kd_matkul: str = Column(String(length=10), ForeignKey("matkul_prak.kd_matkul"))

    matkul_prak = relationship("MatkulPrak", back_populates="jadwal")
