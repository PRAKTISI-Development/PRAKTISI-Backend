from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class MatkulPrak(Base):
    __tablename__ = "matkul_prak"

    kd_matkul: str = Column(String(length=10), primary_key=True, index=True)
    nama_matkul: str = Column(String(length=100), nullable=False)
    usersid: str = Column(String(length=20), ForeignKey("users.userid"))

    user = relationship("User", back_populates="matkul_prak")
    jadwal = relationship("Jadwal", back_populates="matkul_prak")
    kehadiran = relationship("Kehadiran", back_populates="matkul_prak")
    nilai_akhir = relationship("NilaiAkhir", back_populates="matkul_prak")
    tugas = relationship("Tugas", back_populates="matkul_prak")
