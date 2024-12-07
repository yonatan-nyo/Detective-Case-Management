# controllers/case_controller.py
from models.case import Case
from models.database import SessionLocal


class CaseController:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_cases(self):
        return self.db.query(Case).all()

    def get_all_cases_pagination(self, page: int = 1, per_page: int = 10):
        offset = (page - 1) * per_page
        cases = self.db.query(Case).offset(offset).limit(per_page).all()
        # Total number of cases in the database
        total_cases = self.db.query(Case).count()
        return {
            "cases": cases,
            "total_cases": total_cases,
            "current_page": page,
            "total_pages": (total_cases + per_page - 1) // per_page,
        }

    def add_case(self, progress, startDate, description, detective):
        new_case = Case(progress=progress, startDate=startDate,
                        description=description, detective=detective)
        self.db.add(new_case)
        self.db.commit()
        self.db.refresh(new_case)

    def delete_case(self, case_id):
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if case:
            self.db.delete(case)
            self.db.commit()

    def update_case(self, case_id, progress, startDate, description, detective):
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if case:
            case.progress = progress
            case.startDate = startDate
            case.description = description
            case.detective = detective
            self.db.commit()
            self.db.refresh(case)
