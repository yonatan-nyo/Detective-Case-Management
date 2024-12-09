from sqlalchemy import Column, Integer, String, Boolean, Text, select, func
from sqlalchemy.orm import relationship, column_property
from .case_suspect import CaseSuspect
from .database import Base


class Suspect(Base):
    __tablename__ = "suspects"

    id = Column(Integer, primary_key=True, index=True)

    nik = Column(String, nullable=False)
    picture_path = Column(String, nullable=False)
    name = Column(String, nullable=False)

    age = Column(Integer, nullable=False)
    gender = Column(Boolean, nullable=False)
    note = Column(Text, nullable=False)

    cases = relationship('Case', secondary=CaseSuspect,
                         back_populates='suspects')

    cases_count = column_property(
        select(func.count(CaseSuspect.c.case_id))
        .where(CaseSuspect.c.suspect_id == id)
        .scalar_subquery()
    )