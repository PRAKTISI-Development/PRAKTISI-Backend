from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from apps.database import Base
from sqlalchemy.sql import func

class NilaiTugas(Base):
    __tablename__ = "hasil_tugas"

    praktikan_nim = Column(String, ForeignKey("praktikan.nim"), primary_key=True, index=True)
    mata_kuliah_kode_tugas = Column(String, ForeignKey("mata_kuliah.kode_tugas"), primary_key=True, index=True)
    jawaban = Column(String)
    nilai = Column(Integer)
    waktu_pengumpulan = Column(DateTime(timezone=True), default=func.now())

    praktikan = relationship("Praktikan", back_populates="nilai_akhir")
    mata_kuliah = relationship("MataKuliah", back_populates="nilai_akhir")
