from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class User(Base):
    __tablename__ = "users"

    userid: str = Column(String(length=20), primary_key=True, index=True)
    password: str = Column(String(length=100), nullable=False)
    nama: str = Column(String(length=100), nullable=False)
    email: str = Column(String(length=100), nullable=False)
    semester: str = Column(String(length=20), nullable=False)
    praktikan: bool = Column(Boolean, nullable=False)
    asisten_laboratorium: bool = Column(Boolean, nullable=False)
    dosen: bool = Column(Boolean, nullable=False)
    kd_matkul: str = Column(String(length=10), ForeignKey("matkul_prak.kd_matkul"))

    matkul_prak = relationship("MatkulPrak", back_populates="user")
    informasi = relationship("Informasi", back_populates="user")
    kehadiran = relationship("Kehadiran", back_populates="user")
    nilai_akhir = relationship("NilaiAkhir", back_populates="user")
    tugas = relationship("Tugas", back_populates="user")
    detail_pengumpulan = relationship("DetailPengumpulan", back_populates="user")
