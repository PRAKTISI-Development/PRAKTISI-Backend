from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base
from apps.models.kehadiran import Kehadiran

class MatkulPrak(Base):
    __tablename__ = "matkul_prak"

    kd_matkul = Column(String(length=10), primary_key=True, index=True)
    nama_matkul = Column(String(length=100), nullable=False)
    usersid = Column(String(length=20), ForeignKey("users.userid"))

    user = relationship("User", back_populates="matkul_prak", foreign_keys=[usersid], remote_side="User.userid")
    jadwal = relationship("Jadwal", back_populates="matkul_prak")
    # kehadiran = relationship("Kehadiran", back_populates="matkul_prak", foreign_keys=[Kehadiran.matkul_prak_kd_matkul])
    nilai_akhir = relationship("NilaiAkhir", back_populates="matkul_prak")
    tugas = relationship("Tugas", back_populates="matkul_prak")