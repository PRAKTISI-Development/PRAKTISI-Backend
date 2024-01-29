from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from apps.database import Base

class Kehadiran(Base):
    __tablename__ = "kehadiran"

    usersid = Column(String(length=20), ForeignKey("users.userid"), primary_key=True)
    kd_jadwal = Column(String(length=10), ForeignKey("jadwal.kd_jadwal"), primary_key=True)
    keterangan = Column(Enum('Hadir', 'Tidak Hadir'), nullable=False)

    user = relationship(
        "User",
        back_populates="kehadiran",
        primaryjoin="Kehadiran.usersid == User.userid",
        foreign_keys=[usersid]
    )

    jadwal = relationship("Jadwal", back_populates="kehadiran")
