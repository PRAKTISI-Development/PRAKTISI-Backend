from sqlalchemy import Column, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Jadwal(Base):
    __tablename__ = "jadwal"

    kode_jadwal: str = Column(String(length=255), primary_key=True, index=True)
    tanggal: Date = Column(Date)
    waktu: Time = Column(Time)
    ruangan: str = Column(String(length=255))
    mata_kuliah_kode_matkul: str = Column(String(length=255), ForeignKey("mata_kuliah.kode_matkul"))

    mata_kuliah = relationship("MataKuliah", back_populates="jadwal")
