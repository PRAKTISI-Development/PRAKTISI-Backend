from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class User(Base):
    __tablename__ = "users"

    userid = Column(String(length=20), primary_key=True)
    password = Column(String(length=100), nullable=False)
    nama = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False)
    semester = Column(String(length=20), nullable=False)
    praktikan = Column(Boolean, nullable=False)
    asisten_laboratorium = Column(Boolean, nullable=False)
    dosen = Column(Boolean, nullable=False)

    kd_matkul = Column(String(length=10), ForeignKey("matkul_prak.kd_matkul"))
    matkul_prak = relationship("MatkulPrak", back_populates="users", foreign_keys=[kd_matkul],
                               primaryjoin="User.kd_matkul == MatkulPrak.kd_matkul",
                               remote_side="MatkulPrak.kd_matkul")

    nilai_akhir = relationship("NilaiAkhir", back_populates="user")
    detail_pengumpulan = relationship("DetailPengumpulan", back_populates="user")
    kehadiran = relationship("Kehadiran", back_populates="user")
    informasi = relationship("Informasi", back_populates="user")

