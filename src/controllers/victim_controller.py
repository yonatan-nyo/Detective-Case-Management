# controllers/victim_controller.py
from models.victim import Victim
from models.database import SessionLocal
from models.case import Case


class VictimController:
    def __init__(self):
        self.db = SessionLocal()  # Initialize the database session here

    def get_all_victims(self):
        """Get all victims."""
        return self.db.query(Victim).all()

    def get_victim_by_id(self, suspect_id):
        """Retrieve a victim by their ID."""
        return self.db.query(Victim).filter(Victim.id == suspect_id).first()

    def get_victims_by_case(self, case_id):
        """Get all victims associated with a specific case."""
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if case:
            return case.victims  # Assuming victims is a relationship in the Case model
        return []

    def add_victim(self, nik, picture_path, name, age, forensic_result):
        """Add a new victim."""
        new_victim = Victim(
            nik=nik,
            picture_path=picture_path,
            name=name,
            age=age,
            forensic_result=forensic_result
        )
        self.db.add(new_victim)
        self.db.commit()
        self.db.refresh(new_victim)
        return new_victim

    def update_victim(self, victim_id, nik=None, picture_path=None, name=None, age=None, forensic_result=None):
        """Update details of an existing victim."""
        victim = self.db.query(Victim).filter(Victim.id == victim_id).first()
        if victim:
            if nik:
                victim.nik = nik
            if picture_path:
                victim.picture_path = picture_path
            if name:
                victim.name = name
            if age:
                victim.age = age
            if forensic_result:
                victim.forensic_result = forensic_result
            self.db.commit()
            self.db.refresh(victim)
            return victim
        return None

    def delete_victim(self, victim_id):
        """Delete a victim by ID."""
        victim = self.db.query(Victim).filter(Victim.id == victim_id).first()
        if victim:
            self.db.delete(victim)
            self.db.commit()

    def add_victim_to_case(self, victim_id, case_id):
        """Add a victim to a case."""
        case = self.db.query(Case).filter(Case.id == case_id).first()
        victim = self.db.query(Victim).filter(Victim.id == victim_id).first()
        if case and victim:
            case.victims.append(victim)
            self.db.commit()
            self.db.refresh(case)
            return case
        return None

    def remove_victim_from_case(self, victim_id, case_id):
        """Remove a victim from a case."""
        case = self.db.query(Case).filter(Case.id == case_id).first()
        victim = self.db.query(Victim).filter(Victim.id == victim_id).first()
        if case and victim:
            case.victims.remove(victim)
            self.db.commit()
            self.db.refresh(case)
            return case
        return None
    def search_victims(self, name=None, nik=None):
        if name and nik:
            by_name = set(self.db.query(Victim).filter(Victim.name.ilike(f"%{name}%")).all())
            by_nik = set(self.db.query(Victim).filter(Victim.nik.ilike(f"%{nik}%")).all())
            return list(by_name & by_nik)
        if name:
            return self.db.query(Victim).filter(Victim.name.ilike(f"%{name}%")).all()
        if nik:
            return self.db.query(Victim).filter(Victim.nik.ilike(f"%{nik}%")).all()
