from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from apps.database import Base
from sqlalchemy.sql import func

class NilaiTugas(Base):
    __tablename__ = "hasil_tugas"

    praktikan_nim: str = Column(String(length=255), ForeignKey("praktikan.nim"), primary_key=True, index=True)
    mata_kuliah_kode_tugas: str = Column(String(length=255), ForeignKey("mata_kuliah.kode_tugas"), primary_key=True, index=True)
    jawaban: str = Column(String(length=255))
    nilai: int = Column(Integer)
    waktu_pengumpulan: DateTime = Column(DateTime(timezone=True), default=func.now())

    praktikan = relationship("Praktikan", back_populates="nilai_tugas")
    mata_kuliah = relationship("MataKuliah", back_populates="nilai_tugas")
