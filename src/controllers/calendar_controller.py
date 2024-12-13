# controllers/calendar_controller.py
from sqlalchemy import extract
from sqlalchemy.orm import joinedload
from src.models.case import Case
from src.models.database import SessionLocal


class CalendarController:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_cases(self, month, year):
        return self.db.query(Case).outerjoin(Case.victims).outerjoin(Case.suspects).filter(
            extract('year', Case.startDate) == year,
            extract('month', Case.startDate) == month
        ).options(
            joinedload(Case.victims),
            joinedload(Case.suspects)
        ).all()
