import calendar
from datetime import datetime, timedelta

import flet as ft

from src.routes.destinations import destinations
from src.controllers.case_controller import CaseController
from src.controllers.victim_controller import VictimController
from src.controllers.suspect_controller import SuspectController
from src.controllers.calendar_controller import CalendarController


def on_navigation_change(page: ft.Page, selected_index: int):
    """Handles navigation change to display appropriate content."""
    rail = ft.NavigationRail(
        selected_index=selected_index,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=destinations,
        on_change=lambda e: on_navigation_change(
            page, e.control.selected_index),
    )

    if selected_index == 0:
        from src.views.case_view import CaseView
        CaseView().render(page)
    elif selected_index == 1:
        from src.views.suspect_view import SuspectView
        SuspectView().render(page)
    elif selected_index == 2:
        from src.views.victim_view import VictimView
        VictimView().render(page)
    elif selected_index == 3:
        Schedule().render(page)
    elif selected_index == 4:
        from src.views.statistic_view import Statistic
        Statistic().render(page)
    else:
        page.controls.clear()
        page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        content=ft.Text("On Progress", size=24),
                        padding=10,
                        alignment=ft.alignment.center,
                    ),
                ],
                expand=True,
            )
        )
        page.update()


class Schedule:
    def __init__(self):
        self.current_month = int(datetime.now().month)
        self.current_year = int(datetime.now().year)
        self.case_controller = CaseController()
        self.victim_controller = VictimController()
        self.suspect_controller = SuspectController()
        self.calendar_controller = CalendarController()

        # Initialize filter parameters
        self.current_priority = "Semua"
        self.selected_victim = "No Victims"
        self.selected_suspect = "No Suspects"

        # Fetch all cases for the current month and year (initial unfiltered cases)
        self.cases = self.calendar_controller.get_all_cases(
            self.current_month, self.current_year)
        self.filtered_cases = self.cases  # Initially no filtering

    def get_priority_color(self, priority):
        """Returns color based on priority."""
        priority_colors = {
            "Rendah": ft.Colors.GREEN_200,
            "Sedang": ft.Colors.YELLOW_200,
            "Tinggi": ft.Colors.RED_200
        }
        return priority_colors.get(priority, ft.colors.GREY_300)

    def render(self, page):
        """Renders the schedule page."""
        self.page = page

        rail = ft.NavigationRail(
            selected_index=3,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=-0.9,
            destinations=destinations,
            on_change=lambda e: on_navigation_change(
                page, e.control.selected_index),
        )

        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Row(
                    [
                        rail,
                        ft.VerticalDivider(width=1),
                        ft.Container(
                            content=self.create_page(),
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
                bgcolor="#111518",
                expand=True,
            )
        )
        self.page.update()

    def create_page(self):
        """Creates the schedule page with dynamic data from cases, victims, and suspects."""
        victims = self.victim_controller.get_all_victims()
        suspects = self.suspect_controller.get_all_suspects()

        # Prepare victim and suspect options dynamically
        victim_options = [ft.dropdown.Option(
            victim.name) for victim in victims]
        suspect_options = [ft.dropdown.Option(
            suspect.name) for suspect in suspects]

        header = ft.Row(
            [
                ft.Dropdown(
                    label="Bulan",
                    options=[ft.dropdown.Option(month)
                            for month in calendar.month_name[1:]],
                    value=calendar.month_name[self.current_month],
                    width=120,
                    on_change=lambda e: self.update_date(
                        e.control.value, self.current_year),
                ),
                ft.Dropdown(
                    label="Tahun",
                    options=[ft.dropdown.Option(str(year)) for year in range(
                        2000, datetime.now().year + 1)],
                    value=str(self.current_year),
                    width=100,
                    on_change=lambda e: self.update_date(
                        self.current_month, e.control.value),
                ),
                ft.Dropdown(
                    label="Prioritas",
                    options=[ft.dropdown.Option("Semua"), ft.dropdown.Option(
                        "Tinggi"), ft.dropdown.Option("Sedang"), ft.dropdown.Option("Rendah")],
                    value=self.current_priority,
                    width=120,
                    on_change=lambda e: self.update_filter(
                        e.control.value, self.selected_victim, self.selected_suspect),
                ),
                ft.Dropdown(
                    label="Victim",
                    options=victim_options,
                    value=self.selected_victim,
                    width=120,
                    on_change=lambda e: self.update_filter(
                        self.current_priority, e.control.value, self.selected_suspect),
                ),
                ft.Dropdown(
                    label="Suspect",
                    options=suspect_options,
                    value=self.selected_suspect,
                    width=120,
                    on_change=lambda e: self.update_filter(
                        self.current_priority, self.selected_victim, e.control.value),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=15,
        )

        # Generate the calendar days
        calendar_days = []
        first_day_of_month = datetime(self.current_year, self.current_month, 1)
        start_day = first_day_of_month - \
            timedelta(days=first_day_of_month.weekday() + 1)

        # Create a dictionary to map the date to the case IDs
        case_map = {}
        for case in self.filtered_cases:
            case_day = case.startDate.day
            if case.startDate.month == self.current_month and case.startDate.year == self.current_year:
                case_day = case.startDate.day
                if case_day not in case_map:
                    case_map[case_day] = []
                case_map[case_day].append({
                    'id': f"ID: {case.id}",
                    'priority': case.priority
                })

        for i in range(42):
            day = start_day + timedelta(days=i)

            case_texts = []
            if day.month == self.current_month and day.year == self.current_year:
                day_cases = case_map.get(day.day, [])
                for case_info in day_cases:
                    color = self.get_priority_color(case_info['priority'])
                    case_texts.append(
                        ft.Text(
                            case_info['id'],
                            color=color,
                            size=13,
                            weight="bold",
                        )
                    )

            calendar_days.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                str(day.day),
                                color=ft.Colors.WHITE if day.month == self.current_month else ft.Colors.GREY,
                                size=14,
                            ),
                            *case_texts
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=5,
                    ),
                    bgcolor=ft.Colors.BLACK26 if day.month == self.current_month else ft.Colors.BLACK12,
                    width=40,
                    height=40,
                    alignment=ft.alignment.center,
                    padding=10,
                )
            )

        calendar_grid = ft.GridView(
            expand=True,
            runs_count=7,
            child_aspect_ratio=1,
            spacing=5,
            controls=calendar_days,
        )

        # Main content for the page
        content = ft.Column(
            [
                ft.Text("SCHEDULE", size=25, weight="bold",
                        color=ft.Colors.WHITE),
                header,
                ft.Divider(color=ft.Colors.GREY),
                calendar_grid,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            expand=True,
        )

        return content

    def update_date(self, month, year):
        """Updates the current month and year."""
        # Mapping month names in English to numbers
        month_mapping = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12,
        }

        self.current_month = month_mapping.get(month, self.current_month)
        self.current_year = int(year)

        # Fetch all cases for the selected month and year
        self.cases = self.calendar_controller.get_all_cases(
            self.current_month, self.current_year)

        # Apply the current filters to the newly fetched cases
        self.apply_filter()

        self.render(self.page)

    def update_filter(self, priority, victim, suspect):
        """Updates the filter values and re-renders the schedule page."""
        # Update the filter parameters
        self.current_priority = priority
        self.selected_victim = victim
        self.selected_suspect = suspect

        # Apply the filter to the cases
        self.apply_filter()

        # Re-render the page with the updated filter values
        self.render(self.page)

    def apply_filter(self):
        """Applies the selected filters to the cases and stores the filtered cases."""
        self.filtered_cases = [
            case for case in self.cases
            if (
                # Filter by priority
                (self.current_priority == "Semua" or case.priority == self.current_priority) and
                # Filter by victim
                (self.selected_victim == "No Victims" or any(victim.name == self.selected_victim for victim in case.victims)) and
                (self.selected_suspect == "No Suspects" or any(suspect.name ==
                                                               self.selected_suspect for suspect in case.suspects))  # Filter by suspect
            )
        ]

    def get_priority_color(self, priority):
        """Returns color based on priority."""
        priority_colors = {
            "Rendah": ft.Colors.GREEN_900,
            "Sedang": ft.Colors.YELLOW_900,
            "Tinggi": ft.Colors.RED_900
        }
        return priority_colors.get(priority, ft.Colors.GREY_300)
