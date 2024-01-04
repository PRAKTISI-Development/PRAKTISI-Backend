from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Jadwal(Base):
    __tablename__ = "jadwal"

    kode_jadwal = Column(String, primary_key=True, index=True)
    tanggal = Column(Date)
    waktu = Column(String)
    ruangan = Column(String)
    mata_kuliah_kode_matkul = Column(String, ForeignKey("mata_kuliah.kode_matkul"))

    mata_kuliah = relationship("MataKuliah", back_populates="jadwal")
