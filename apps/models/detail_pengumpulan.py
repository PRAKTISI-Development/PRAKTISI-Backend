import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class DetailPengumpulan(Base):
    __tablename__ = 'detail_pengumpulan'
    id = Column(Integer, primary_key=True)
    usersid = Column(String(length=20), ForeignKey('users.userid'))
    kd_tugas = Column(String(length=10), ForeignKey('tugas.kd_tugas'))
    tanggal_dikumpul = Column(DateTime, nullable=False, default=datetime.datetime.now())
    link_tugas = Column(Text, nullable=True)
    nilai_tugas = Column(Integer, nullable=False, default=0)
    file_path = Column(Text,nullable=False)

    user = relationship('User', back_populates='detail_pengumpulan')
    tugas = relationship('Tugas', back_populates='detail_pengumpulan')
