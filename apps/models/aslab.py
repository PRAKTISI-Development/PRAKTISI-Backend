from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Aslab(Base):
    __tablename__ = "aslab"

    nim: str = Column(String, primary_key=True, index=True)
    mata_kuliah_kode_matkul: str = Column(String, ForeignKey("mata_kuliah.kode_matkul"))

    user = relationship("User", back_populates="aslab")
    mata_kuliah = relationship("MataKuliah", back_populates="aslab")
