from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from .case_victim import CaseVictim
from .case_suspect import CaseSuspect
from .database import Base


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    progress = Column(Integer, nullable=False)
    startDate = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    detective = Column(String, nullable=True)

    victims = relationship(
        'Victim', secondary=CaseVictim, back_populates="cases")
    suspects = relationship(
        'Suspect', secondary=CaseSuspect, back_populates='cases')
