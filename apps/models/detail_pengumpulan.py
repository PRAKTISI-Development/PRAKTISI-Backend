from datetime import datetime
from sqlalchemy import CHAR, Column, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class DetailPengumpulan(Base):
    __tablename__ = "detail_pengumpulan"

    usersid = Column(CHAR(length=20), ForeignKey("users.userid"), primary_key=True, index=True)
    kd_tugas = Column(CHAR(length=10), ForeignKey("tugas.kd_tugas"), primary_key=True, index=True)
    tanggal_dikumpul = Column(DateTime, nullable=False, default=datetime.utcnow)
    file_tugas = Column(Text, nullable=False)
    nilai_tugas = Column(Integer, nullable=False)

    # Gunakan Mapped[] untuk menentukan tipe relasi
    user = relationship("User", back_populates="detail_pengumpulan", uselist=False)
    tugas = relationship("Tugas", back_populates="detail_pengumpulan", uselist=False)
