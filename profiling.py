import cProfile

from src.controllers.calendar_controller import CalendarController
from src.controllers.case_controller import CaseController
from src.controllers.suspect_controller import SuspectController
from src.controllers.victim_controller import VictimController

caseController = CaseController()
suspectController = SuspectController()
victimController = VictimController()
calendarController = CalendarController()


def benchmark():
    """Function to benchmark the controllers' methods."""
    caseController.get_all_cases_pagination(1, 12, None)
    suspectController.get_all_suspects()
    victimController.get_all_victims()
    calendarController.get_all_cases(12, 2024)


if __name__ == '__main__':
    # Use cProfile to benchmark the benchmark function
    cProfile.run('benchmark()')
