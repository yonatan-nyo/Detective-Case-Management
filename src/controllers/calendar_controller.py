# controllers/case_controller.py
from models.case import Case
from models.database import SessionLocal
from sqlalchemy import extract
from sqlalchemy.orm import joinedload


class CalendarController:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_cases(self, month, year):
        return self.db.query(Case).join(Case.victims).join(Case.suspects).filter(
            extract('year', Case.startDate) == year,
            extract('month', Case.startDate) == month
        ).options(
            joinedload(Case.victims),
            joinedload(Case.suspects)
        ).all()
