from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base
from apps.models.users import User

class MatkulPrak(Base):
    __tablename__ = "matkul_prak"

    kd_matkul = Column(String(length=10), primary_key=True, index=True)
    nama_matkul = Column(String(length=100), nullable=False)

    user = relationship("User", back_populates="matkul_prak", foreign_keys=[User.kd_matkul])
    jadwal = relationship("Jadwal", back_populates="matkul_prak")
    kehadiran = relationship("Kehadiran", back_populates="matkul_prak")
    nilai_akhir = relationship("NilaiAkhir", back_populates="matkul_prak")
    tugas = relationship("Tugas", back_populates="matkul_prak")
