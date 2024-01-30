from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from apps.database import Base

class Kehadiran(Base):
    __tablename__ = 'kehadiran'

    usersid = Column(String(length=20), ForeignKey('users.userid'), primary_key=True)
    tanggal_kehadiran = Column(DateTime, primary_key=True)
    status_kehadiran = Column(String(length=10), nullable=False)  

    user = relationship('User', back_populates='kehadiran')
