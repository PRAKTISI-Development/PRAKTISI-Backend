from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from apps.database import Base

class Kehadiran(Base):
    __tablename__ = "kehadiran"

    usersid = Column(String(length=20), ForeignKey("users.userid"), primary_key=True)
    kd_jadwal = Column(String(length=10), ForeignKey("jadwal.kd_jadwal"), primary_key=True)
    pertemuan = Column(Integer, nullable=False)
    materi = Column(String(length=100), nullable=False)
    tanggal = Column(DateTime, nullable=False)
    keterangan = Column(Enum('Hadir', 'Tidak Hadir'), nullable=False)
    
    # Define the direct foreign key relationship
    matkul_prak_kd_matkul = Column(String(length=10), ForeignKey("matkul_prak.kd_matkul"))

    # Define the relationship with the MatkulPrak model
    matkul_prak = relationship(
        "MatkulPrak",
        back_populates="kehadiran",
        primaryjoin="Kehadiran.matkul_prak_kd_matkul == MatkulPrak.kd_matkul",
        foreign_keys=[matkul_prak_kd_matkul]
    )

    # Define the relationship with the User model
    user = relationship(
        "User",
        back_populates="kehadiran",
        primaryjoin="Kehadiran.usersid == User.userid",
        foreign_keys=[usersid]
    )

    # Define the relationship with the Jadwal model
    jadwal = relationship("Jadwal", back_populates="kehadiran")
