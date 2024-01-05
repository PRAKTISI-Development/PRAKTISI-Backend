from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from apps.database import Base

class Praktikan(Base):
    __tablename__ = "praktikan"

    nim: str = Column(String, primary_key=True, index=True)

    user: str = relationship("User", back_populates="praktikan")
    nilai_akhir: int = relationship("NilaiAkhir", back_populates="praktikan")
