from sqlalchemy import Column, Integer, String, Text, select, func
from sqlalchemy.orm import relationship, column_property
from .case_victim import CaseVictim
from .database import Base


class Victim(Base):
    __tablename__ = "victims"

    id = Column(Integer, primary_key=True, index=True)

    nik = Column(String, nullable=False)
    picture_path = Column(String, nullable=False)
    name = Column(String, nullable=False)

    age = Column(Integer, nullable=False)
    forensic_result = Column(Text, nullable=False)

    cases = relationship('Case', secondary=CaseVictim,
                         back_populates='victims')
