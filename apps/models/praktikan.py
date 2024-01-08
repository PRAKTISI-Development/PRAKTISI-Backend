from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Praktikan(Base):
    __tablename__ = "praktikan"

    nim = Column(String, ForeignKey("user.nim"), primary_key=True, index=True)

    user = relationship("User", back_populates="praktikan")
    nilai_akhir = relationship("NilaiAkhir", back_populates="praktikan")
