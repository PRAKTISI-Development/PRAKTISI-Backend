from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class NilaiAkhir(Base):
    __tablename__ = 'nilai_akhir'

    usersid = Column(String(length=20), ForeignKey('users.userid'), primary_key=True)
    kd_matkul = Column(String(length=10), ForeignKey('matkul_prak.kd_matkul'), primary_key=True)
    nilai_akhir = Column(Integer)

    user = relationship('User', back_populates='nilai_akhir', foreign_keys=[usersid])
    matkul_prak = relationship('MatkulPrak', back_populates='nilai_akhir', foreign_keys=[kd_matkul])