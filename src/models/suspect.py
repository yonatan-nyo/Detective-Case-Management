from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from .case_suspect import CaseSuspect
from .database import Base


class Suspect(Base):
    __tablename__ = "suspects"

    id = Column(Integer, primary_key=True, index=True)

    nik = Column(String, nullable=False)
    picturePath = Column(String, nullable=False)
    name = Column(String, nullable=False)

    age = Column(Integer, nullable=False)
    gender = Column(Boolean, nullable=False)
    note = Column(Text, nullable=False)

    cases = relationship('Case', secondary=CaseSuspect,
                         back_populates='suspects')
