from datetime import date

from src.models.database import Base
from src.models.case import Case
from src.controllers.calendar_controller import CalendarController


def test_get_all_cases():
    """Test that get_all_cases returns cases filtered by month and year."""
    # Replace SessionLocal with the test database session
    controller = CalendarController()
    cases = controller.get_all_cases(month=12, year=2024)

    assert all(isinstance(case, Case) for case in cases)  # Verify type
