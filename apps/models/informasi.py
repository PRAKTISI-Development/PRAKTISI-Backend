from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Informasi(Base):
    __tablename__ = 'informasi'

    kd_informasi = Column(String(length=5), primary_key=True)
    tanggal = Column(DateTime, nullable=False)
    judul_informasi = Column(String(length=50), nullable=False)
    deskripsi_informasi = Column(Text, nullable=False)
    tautan = Column(Text)
    usersid = Column(String(length=20), ForeignKey('users.userid'))

    user = relationship('User', back_populates='informasi')
