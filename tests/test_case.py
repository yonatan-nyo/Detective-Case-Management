from datetime import date
from src.models.case import Case
from src.controllers.case_controller import CaseController

controller = CaseController()


def test_get_all_cases():
    """Test that get_all_cases returns all cases."""
    cases = controller.get_all_cases()
    assert all(isinstance(case, Case) for case in cases)


def test_get_all_cases_pagination():
    """Test that get_all_cases_pagination returns paginated cases."""
    pagination_result = controller.get_all_cases_pagination(page=1, per_page=5)
    assert isinstance(pagination_result, dict)
    assert 'cases' in pagination_result
    assert 'total_cases' in pagination_result
    assert 'current_page' in pagination_result
    assert 'total_pages' in pagination_result
    assert len(pagination_result['cases']) <= 5


def test_add_case():
    """Test that add_case adds a new case to the database."""
    # get all cases
    cases = controller.get_all_cases()
    length = len(cases)

    controller.add_case(progress=0, startDate=date(
        2024, 12, 1), description="New Case", detective="John Doe", priority=1)

    # get all cases again
    cases = controller.get_all_cases()
    assert len(cases) == length + 1
