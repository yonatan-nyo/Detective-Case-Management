# controllers/victim_controller.py
from models.victim import Victim
from models.database import SessionLocal
from models.case import Case


class VictimController:
    def _init_(self):
        self.db = SessionLocal()

    def get_all_victims(self):
        """Get all victims."""
        return self.db.query(Victim).all()

    def get_victims_by_case(self, case_id):
        """Get all victims associated with a specific case."""
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if case:
            return case.victims  # Assuming victims is a relationship in the Case model
        return []

    def add_victim(self, nik, picturePath, name, age, forensicResult):
        """Add a new victim."""
        new_victim = Victim(
            nik=nik,
            picturePath=picturePath,
            name=name,
            age=age,
            forensicResult=forensicResult
        )
        self.db.add(new_victim)
        self.db.commit()
        self.db.refresh(new_victim)
        return new_victim

    def update_victim(self, victim_id, nik=None, picturePath=None, name=None, age=None, forensicResult=None):
        """Update details of an existing victim."""
        victim = self.db.query(Victim).filter(Victim.id == victim_id).first()
        if victim:
            if nik:
                victim.nik = nik
            if picturePath:
                victim.picturePath = picturePath
            if name:
                victim.name = name
            if age:
                victim.age = age
            if forensicResult:
                victim.forensicResult = forensicResult
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