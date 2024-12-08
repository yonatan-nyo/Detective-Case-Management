from models.suspect import Suspect
from models.database import SessionLocal
from models.case import Case


class SuspectController:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_suspects(self):
        """Get all suspects."""
        return self.db.query(Suspect).all()

    def get_suspect_by_id(self, suspect_id):
        """Retrieve a suspect by their ID."""
        return self.db.query(Suspect).filter(Suspect.id == suspect_id).first()

    def get_suspects_by_case(self, case_id):
        """Get all suspects associated with a specific case."""
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if case:
            return case.suspects  # Assuming suspects is a relationship in the Case model
        return []

    def add_suspect(self, nik, picture_path, name, age, gender, note):
        """Add a new suspect."""
        new_suspect = Suspect(
            nik=nik,
            picture_path=picture_path,
            name=name,
            age=age,
            gender=(gender == "True"),
            note=note
        )
        self.db.add(new_suspect)
        self.db.commit()
        self.db.refresh(new_suspect)
        return new_suspect

    def update_suspect(self, suspect_id, nik=None, picture_path=None, name=None, age=None, gender=None, note=None):
        """Update details of an existing suspect."""
        suspect = self.db.query(Suspect).filter(
            Suspect.id == suspect_id).first()
        if suspect:
            if nik:
                suspect.nik = nik
            if picture_path:
                suspect.picture_path = picture_path
            if name:
                suspect.name = name
            if age:
                suspect.age = age
            if gender is not None:
                suspect.gender = (gender == "True")
            if note:
                suspect.note = note
            self.db.commit()
            self.db.refresh(suspect)
            return suspect
        return None

    def delete_suspect(self, suspect_id):
        """Delete a suspect by ID."""
        suspect = self.db.query(Suspect).filter(
            Suspect.id == suspect_id).first()
        if suspect:
            self.db.delete(suspect)
            self.db.commit()

    def add_suspect_to_case(self, suspect_id, case_id):
        """Add a suspect to a case."""
        case = self.db.query(Case).filter(Case.id == case_id).first()
        suspect = self.db.query(Suspect).filter(
            Suspect.id == suspect_id).first()
        if case and suspect:
            case.suspects.append(suspect)
            self.db.commit()
            self.db.refresh(case)
            return case
        return None

    def remove_suspect_from_case(self, suspect_id, case_id):
        """Remove a suspect from a case."""
        case = self.db.query(Case).filter(Case.id == case_id).first()
        suspect = self.db.query(Suspect).filter(
            Suspect.id == suspect_id).first()
        if case and suspect:
            case.suspects.remove(suspect)
            self.db.commit()
            self.db.refresh(case)
            return case
        return None
