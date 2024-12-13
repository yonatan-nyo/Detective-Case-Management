from src.models.victim import Victim
from src.controllers.victim_controller import VictimController

controller = VictimController()


def test_get_all_victims():
    """Test that get_all_victims returns all victims."""
    victims = controller.get_all_victims()
    assert isinstance(victims, list)
    assert all(isinstance(victim, Victim) for victim in victims)


def test_get_victim_by_id():
    """Test that get_victim_by_id returns a victim by their ID."""
    victim = controller.get_victim_by_id(
        1)  # Assuming a victim with ID 1 exists
    assert isinstance(victim, Victim)
    assert victim.id == 1


def test_add_victim():
    """Test that add_victim adds a new victim to the database."""
    # get all victims before adding
    victims = controller.get_all_victims()
    length = len(victims)

    controller.add_victim(
        nik="123456", picture_path="/path/to/picture", name="John Doe", age=30, forensic_result="Poisoning"
    )

    # get all victims after adding
    victims = controller.get_all_victims()
    assert len(victims) == length + 1
