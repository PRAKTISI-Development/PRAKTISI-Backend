from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class NilaiAkhir(Base):
    __tablename__ = "nilai_akhir"

    usersid: str = Column(String(length=20), ForeignKey("users.userid"), primary_key=True, index=True)
    kd_matkul: str = Column(String(length=10), ForeignKey("matkul_prak.kd_matkul"), primary_key=True, index=True)
    nilai_akhir: int = Column(Integer)

    user = relationship("User", back_populates="nilai_akhir")
    matkul_prak = relationship("MatkulPrak", back_populates="nilai_akhir")
