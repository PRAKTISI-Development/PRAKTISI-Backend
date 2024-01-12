from datetime import datetime
from sqlalchemy import Column, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Informasi(Base):
    __tablename__ = "informasi"

    kd_informasi: str = Column(String(length=5), primary_key=True, index=True)
    tanggal: datetime = Column(DateTime, nullable=False)
    judul_informasi: str = Column(String(length=50), nullable=False)
    deskripsi_informasi: str = Column(Text, nullable=False)
    tautan: str = Column(Text)
    usersid: str = Column(String(length=20), ForeignKey("users.userid"))

    user = relationship("User", back_populates="informasi")
