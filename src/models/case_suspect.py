from sqlalchemy import Table, ForeignKey, Column
from .database import Base

CaseSuspect = Table(
    "case_suspects",
    Base.metadata,
    Column("case_id", ForeignKey("cases.id"), primary_key=True),
    Column("suspect_id", ForeignKey("suspects.id"), primary_key=True),
)
