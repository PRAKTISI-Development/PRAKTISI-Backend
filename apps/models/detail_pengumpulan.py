from datetime import datetime
from sqlalchemy import String, Column, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class DetailPengumpulan(Base):
    __tablename__ = "detail_pengumpulan"

    usersid: str = Column(String(length=20), ForeignKey("users.userid"), primary_key=True, index=True)
    kd_tugas: str = Column(String(length=10), ForeignKey("tugas.kd_tugas"), primary_key=True, index=True)
    tanggal_dikumpul: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    file_tugas: str = Column(Text, nullable=False)
    nilai_tugas: int = Column(Integer, nullable=False)

    user = relationship("User", back_populates="detail_pengumpulan")
    tugas = relationship("Tugas", back_populates="detail_pengumpulan")
