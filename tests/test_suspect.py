from src.models.suspect import Suspect
from src.controllers.suspect_controller import SuspectController

controller = SuspectController()


def test_get_all_suspects():
    """Test that get_all_suspects returns all suspects."""
    suspects = controller.get_all_suspects()
    assert isinstance(suspects, list)
    assert all(isinstance(suspect, Suspect) for suspect in suspects)


def test_get_suspect_by_id():
    """Test that get_suspect_by_id returns a suspect by their ID."""
    suspect = controller.get_suspect_by_id(
        1)  # Assuming a suspect with ID 1 exists
    if (suspect):
        assert suspect.id == 1


def test_add_suspect():
    """Test that add_suspect adds a new suspect to the database."""
    # get all suspects before adding
    suspects = controller.get_all_suspects()
    length = len(suspects)

    controller.add_suspect(
        nik="123456", picture_path="/path/to/picture", name="John Doe", age=30, gender="True", note="Suspicious"
    )

    # get all suspects after adding
    suspects = controller.get_all_suspects()
    assert len(suspects) == length + 1
