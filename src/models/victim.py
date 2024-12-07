from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .case_victim import CaseVictim
from .database import Base


class Victim(Base):
    __tablename__ = "victims"

    id = Column(Integer, primary_key=True, index=True)

    nik = Column(String, nullable=False)
    picturePath = Column(String, nullable=False)
    name = Column(String, nullable=False)

    age = Column(Integer, nullable=False)
    forensicResult = Column(Text, nullable=False)

    cases = relationship('Case', secondary=CaseVictim,
                         back_populates='victims')
