from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from apps.database import Base

class Kehadiran(Base):
    __tablename__ = 'kehadiran'

    usersid = Column(String(length=20), ForeignKey('users.userid'), primary_key=True)
    status = Column(String(length=10), nullable=False) 
    keterangan = Column(String(length=100), nullable=False) 
    

    kd_jadwal = Column(String(length=5), ForeignKey('jadwal.kd_jadwal'), primary_key=True) 

    jadwal = relationship('Jadwal', back_populates='kehadiran', primaryjoin="Jadwal.kd_jadwal == Kehadiran.kd_jadwal")

    user = relationship('User', back_populates='kehadiran')
