from sqlalchemy import Table, ForeignKey, Column
from .database import Base


CaseVictim = Table(
    "case_victims",
    Base.metadata,
    Column("case_id", ForeignKey("cases.id"), primary_key=True),
    Column("victim_id", ForeignKey("victims.id"), primary_key=True),
)
