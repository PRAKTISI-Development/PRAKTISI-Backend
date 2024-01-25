import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class DetailPengumpulan(Base):
    __tablename__ = 'detail_pengumpulan'

    usersid = Column(String(length=20), ForeignKey('users.userid'), primary_key=True)
    kd_tugas = Column(String(length=10), ForeignKey('tugas.kd_tugas'), primary_key=True)
    tanggal_dikumpul = Column(DateTime, nullable=False, default=datetime.datetime.now())
    file_tugas = Column(Text, nullable=False)
    nilai_tugas = Column(Integer, nullable=False, default=0)

    user = relationship('User', back_populates='detail_pengumpulan')
    tugas = relationship('Tugas', back_populates='detail_pengumpulan')
