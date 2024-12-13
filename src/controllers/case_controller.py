# controllers/case_controller.py
from src.models.case import Case
from src.models.database import SessionLocal
from src.models.victim import Victim
from src.models.suspect import Suspect


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

    def add_case(self, progress, startDate, description, detective, priority):
        new_case = Case(progress=progress, startDate=startDate,
                        description=description, detective=detective, priority=priority)
        self.db.add(new_case)
        self.db.commit()
        self.db.refresh(new_case)

    def delete_case(self, case_id):
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if case:
            self.db.delete(case)
            self.db.commit()

    def update_case(self, case_id, progress, startDate, description, detective, priority):
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if case:
            case.progress = progress
            case.startDate = startDate
            case.description = description
            case.detective = detective
            case.priority = priority
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

    def get_top_ten_suspects(self):
        """Retrieve top 10 suspects by number of cases they are involved in."""
        from sqlalchemy import func

        # Create a subquery to count cases per suspect
        suspect_case_counts = (
            self.db.query(Suspect.id, Suspect.name,
                          func.count(Case.id).label('cases_count'))
            .join(Case.suspects)
            .group_by(Suspect.id, Suspect.name)
            .order_by(func.count(Case.id).desc())
            .limit(10)
            .all()
        )

        # Convert results to a list of objects with name and cases_count attributes
        return [
            type('SuspectStats', (), {
                'id': suspect[0],
                'name': suspect[1],
                'cases_count': suspect[2]
            })() for suspect in suspect_case_counts
        ]

    def get_top_ten_victims(self):
        """Retrieve top 10 victims by number of cases they are involved in."""
        from sqlalchemy import func

        # Create a subquery to count cases per victim
        victim_case_counts = (
            self.db.query(Victim.id, Victim.name, func.count(
                Case.id).label('cases_count'))
            .join(Case.victims)
            .group_by(Victim.id, Victim.name)
            .order_by(func.count(Case.id).desc())
            .limit(10)
            .all()
        )

        # Convert results to a list of objects with name and cases_count attributes
        return [
            type('VictimStats', (), {
                'id': victim[0],
                'name': victim[1],
                'cases_count': victim[2]
            })() for victim in victim_case_counts
        ]
