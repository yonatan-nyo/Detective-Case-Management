# controllers/case_controller.py
from models.case import Case
from models.database import SessionLocal
from models.victim import Victim
from models.suspect import Suspect


class CaseController:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_cases(self):
        return self.db.query(Case).all()

    def get_case_by_id(self, case_id):
        """Retrieves a case by its ID."""
        return self.db.query(Case).filter(Case.id == case_id).first()

    def get_all_cases_pagination(self, page: int = 1, per_page: int = 10, filter_progress: int = None):
        """Fetches paginated cases, optionally filtering by progress."""
        offset = (page - 1) * per_page

        # Build base query
        query = self.db.query(Case)

        # Apply filter if filter_progress is provided
        if filter_progress is not None:
            query = query.filter(Case.progress == filter_progress)

        # Fetch filtered and paginated cases
        cases = query.offset(offset).limit(per_page).all()

        # Total number of cases in the database (considering the filter)
        total_cases = query.count()

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

    def get_unassigned_suspects(self, case_id):
        """Retrieve suspects not yet assigned to this case."""
        case = self.get_case_by_id(case_id)

        if not case:
            return []

        # Get IDs of suspects already assigned to this case
        assigned_suspect_ids = [suspect.id for suspect in case.suspects]

        # If no suspects are assigned, return all suspects
        if not assigned_suspect_ids:
            return self.db.query(Suspect).all()

        # Return suspects not in the assigned list
        return self.db.query(Suspect).filter(Suspect.id.notin_(assigned_suspect_ids)).all()

    def assign_suspect_to_case(self, case_id, suspect_id):
        """Assign a suspect to a specific case."""
        case = self.get_case_by_id(case_id)
        suspect = self.db.query(Suspect).filter(
            Suspect.id == suspect_id).first()

        if case and suspect:
            case.suspects.append(suspect)
            self.db.commit()

    def remove_suspect_from_case(self, case_id, suspect_id):
        """Remove a suspect from a specific case."""
        case = self.get_case_by_id(case_id)
        suspect = self.db.query(Suspect).filter(
            Suspect.id == suspect_id).first()

        if case and suspect:
            case.suspects.remove(suspect)
            self.db.commit()

    def get_unassigned_victims(self, case_id):
        """Retrieve victims not yet assigned to this case."""
        case = self.get_case_by_id(case_id)

        if not case:
            return []

        # Get IDs of victims already assigned to this case
        assigned_victim_ids = [victim.id for victim in case.victims]

        # If no victims are assigned, return all victims
        if not assigned_victim_ids:
            return self.db.query(Victim).all()

        # Return victims not in the assigned list
        return self.db.query(Victim).filter(Victim.id.notin_(assigned_victim_ids)).all()

    def assign_victim_to_case(self, case_id, victim_id):
        """Assign a victim to a specific case."""
        case = self.get_case_by_id(case_id)
        victim = self.db.query(Victim).filter(Victim.id == victim_id).first()

        if case and victim:
            case.victims.append(victim)
            self.db.commit()

    def remove_victim_from_case(self, case_id, victim_id):
        """Remove a victim from a specific case."""
        case = self.get_case_by_id(case_id)
        victim = self.db.query(Victim).filter(Victim.id == victim_id).first()

        if case and victim:
            case.victims.remove(victim)
            self.db.commit()
