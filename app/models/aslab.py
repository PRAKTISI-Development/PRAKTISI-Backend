from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Aslab(Base):
    __tablename__ = "aslab"

    nim = Column(String, primary_key=True, index=True)
    mata_kuliah_kode_matkul = Column(String, ForeignKey("mata_kuliah.kode_matkul"))

    mata_kuliah = relationship("MataKuliah", back_populates="aslab")
