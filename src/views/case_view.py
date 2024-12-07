# views/case_view.py
import flet as ft
from controllers.case_controller import CaseController
from datetime import date

from routes.destinations import destinations


def on_navigation_change(page: ft.Page, selected_index: int):
    page.floating_action_button = None
    """Handles navigation change to display appropriate content."""
    # if selected_index == 0:  # Manajemen Kasus
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
        CaseView().render(page)
    elif selected_index == 1:
        from views.suspect_view import SuspectView
        SuspectView().render(page)
    elif selected_index == 2:
        from views.victim_view import VictimView
        VictimView().render(page)
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


class CaseView:
    def __init__(self):
        self.controller = CaseController()
        self.page = None
        self.page_number = 1
        self.per_page = 12
        self.total_pages = 1  # Initialize total pages

    def fetch_cases(self):
        """Fetches cases for the current page."""
        pagination_data = self.controller.get_all_cases_pagination(
            page=self.page_number, per_page=self.per_page
        )
        self.total_pages = pagination_data["total_pages"]
        return pagination_data["cases"]

    def build_cases_component(self, cases):
        """Builds the cases component with the given list of cases."""
        temp_row = []
        for _idx, case in enumerate(cases):
            def on_hover(e):
                e.control.bgcolor = "black" if e.data == "true" else ft.Colors.BLACK54
                e.control.update()

            def on_tap_down(_e: ft.ContainerTapEvent, idx=_idx):
                self.render_detail(cases[idx].id)

            case_card = (
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"ID: {case.id}", size=12),
                            ft.Text(f"Progress: {case.progress}", size=14),
                            ft.Text(f"Start Date: {case.startDate}", size=12),
                            ft.Text(f"Detective: {case.detective}", size=12),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor=ft.Colors.BLACK54,
                    on_hover=on_hover,
                    on_tap_down=lambda e, idx=_idx: on_tap_down(e, idx),
                    padding=10,
                    expand=False,
                )
            )

            temp_row.append(
                ft.Container(
                    case_card,
                    padding=5,
                    col={"sm": 6, "md": 4, "xl": 3},
                )
            )

        return ft.ResponsiveRow(temp_row, expand=False)

    def build_pagination_controls(self):
        """Builds pagination controls."""
        return ft.Row(
            [
                ft.ElevatedButton(
                    "Previous",
                    on_click=self.previous_page,
                    disabled=self.page_number <= 1,
                ),
                ft.Text(f"Page {self.page_number} of {self.total_pages}"),
                ft.ElevatedButton(
                    "Next",
                    on_click=self.next_page,
                    disabled=self.page_number >= self.total_pages,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def previous_page(self, _e):
        """Handles the Previous button click."""
        if self.page_number > 1:
            self.page_number -= 1
            self.render(self.page)

    def next_page(self, _e):
        """Handles the Next button click."""
        if self.page_number < self.total_pages:
            self.page_number += 1
            self.render(self.page)

    def render(self, page: ft.Page):
        """Renders the case management view."""
        self.page = page
        cases = self.fetch_cases()

        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=-0.9,
            destinations=destinations,
            on_change=lambda e: on_navigation_change(
                page, e.control.selected_index
            ),
        )

        self.page.controls.clear()
        self.page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Text("Case Management", size=24),
                                padding=10,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                [self.build_cases_component(cases)],
                                expand=True,
                            ),
                            self.build_pagination_controls(),
                        ],
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )

        def fab_pressed(e):
            self.render_add_case()
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, on_click=fab_pressed, bgcolor=ft.Colors.BLUE_GREY_700)
        self.page.update()

    def render_add_case(self):
        """Renders the Add Case form with correct data types."""

        # To store the selected date
        selected_date = ft.TextField(
            label="Start Date", read_only=True, hint_text="Select a date")

        def handle_date_change(e):
            """Handles the date selection."""
            if e.control.value:
                selected_date.value = e.control.value.strftime("%Y-%m-%d")
                self.page.update()

        def button_clicked(e):
            """Handles form submission."""
            # Get progress as integer from dropdown
            try:
                progress = int(progress_field.value)
            except (ValueError, TypeError):
                progress_field.error_text = "Please select a valid progress."
                self.page.update()
                return

            # Validate selected date
            if not selected_date.value:
                selected_date.error_text = "Please select a valid date."
                self.page.update()
                return
            try:
                start_date = date.fromisoformat(
                    selected_date.value)  # Use date here
            except ValueError:
                selected_date.error_text = "Invalid date format (expected YYYY-MM-DD)."
                self.page.update()
                return

            # Get other fields
            description = description_field.value
            detective = detective_field.value

            # Validate description
            if not description.strip():
                description_field.error_text = "Description cannot be empty."
                self.page.update()
                return

            # Add the new case using the controller
            self.controller.add_case(
                progress, start_date, description, detective)

            # After submitting, render the case management view again
            self.render(self.page)

        # Create form fields
        progress_field = ft.Dropdown(
            label="Progress",
            options=[
                ft.dropdown.Option(key=0, text="On-going"),
                ft.dropdown.Option(key=1, text="Solved"),
                ft.dropdown.Option(key=2, text="Unsolved"),
            ],
        )
        date_picker_button = ft.ElevatedButton(
            "Pick Date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=date(2023, 1, 1),
                    last_date=date(2024, 12, 31),
                    on_change=handle_date_change,
                )
            ),
        )
        description_field = ft.TextField(label="Description", multiline=True)
        detective_field = ft.TextField(label="Detective")

        # Submit button
        submit_button = ft.ElevatedButton(
            text="Add Case",
            on_click=button_clicked,
        )

        def go_back(e):
            """Handles the back button click."""
            self.render(self.page)

        # Add the form fields and buttons to the page
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        progress_field,
                        ft.Row([selected_date, date_picker_button],
                               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        description_field,
                        detective_field,
                        submit_button,
                        ft.ElevatedButton(
                            text="Back",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=go_back,
                        ),
                    ],
                    width=700,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=10,
                expand=True,
                alignment=ft.alignment.center,
            )
        )
        self.page.update()

    def render_detail(self, case_id):
        """Renders the details of a specific case."""
        # Fetch case details using the controller
        case = self.controller.get_case_by_id(case_id)
        if not case:
            # If the case doesn't exist, show an error message
            self.page.controls.clear()
            self.page.add(
                ft.Container(
                    content=ft.Text("Case not found.", size=24),
                    alignment=ft.alignment.center,
                    padding=10,
                )
            )
            self.page.update()
            return

        def go_back(e):
            """Handles the back button click."""
            self.render(self.page)

        def update_case(e):
            """Handles the update button click."""
            self.render_update_case(case)

        def delete_case(e):
            """Handles the delete button click."""
            self.controller.delete_case(case_id)
            self.render(self.page)

        # Display case details
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Case Details", size=24, weight="bold"),
                        ft.Row(
                            [
                                ft.Text("Case ID:", size=16, weight="bold"),
                                ft.Text(case.id, size=16),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Text("Progress:", size=16, weight="bold"),
                                ft.Text(case.progress, size=16),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Text("Start Date:", size=16, weight="bold"),
                                ft.Text(case.startDate, size=16),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Text("Detective:", size=16, weight="bold"),
                                ft.Text(case.detective, size=16),
                            ]
                        ),
                        ft.Container(
                            content=ft.Text(
                                f"Description:\n{case.description}",
                                size=16,
                                weight="normal",
                            ),
                            padding=10,
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text="Update",
                                    icon=ft.Icons.EDIT,
                                    on_click=update_case,
                                ),
                                ft.ElevatedButton(
                                    text="Delete",
                                    icon=ft.Icons.DELETE,
                                    on_click=delete_case,
                                    bgcolor=ft.Colors.RED_600,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.ElevatedButton(
                            text="Back",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=go_back,
                        ),
                    ],
                    expand=True,
                ),
                padding=20,
                alignment=ft.alignment.center,
            )
        )
        self.page.update()

    def render_update_case(self, case):
        """Renders the Update Case form with current data pre-filled."""

        # To store the selected date
        selected_date = ft.TextField(
            label="Start Date", read_only=True, hint_text="Select a date", value=case.startDate
        )

        def handle_date_change(e):
            """Handles the date selection."""
            if e.control.value:
                selected_date.value = e.control.value.strftime("%Y-%m-%d")
                self.page.update()

        def button_clicked(e):
            """Handles form submission for updating the case."""
            # Get progress as integer from dropdown
            try:
                progress = int(progress_field.value)
            except (ValueError, TypeError):
                progress_field.error_text = "Please select a valid progress."
                self.page.update()
                return

            # Validate selected date
            if not selected_date.value:
                selected_date.error_text = "Please select a valid date."
                self.page.update()
                return
            try:
                start_date = date.fromisoformat(
                    str(selected_date.value))  # Use date here
            except ValueError:
                selected_date.error_text = "Invalid date format (expected YYYY-MM-DD)."
                self.page.update()
                return

            # Get other fields
            description = description_field.value
            detective = detective_field.value

            # Validate description
            if not description.strip():
                description_field.error_text = "Description cannot be empty."
                self.page.update()
                return

            # Update the case using the controller
            self.controller.update_case(
                case.id, progress, start_date, description, detective
            )

            # After submitting, render the case management view again
            self.render(self.page)

        # Create form fields pre-filled with existing case details
        progress_field = ft.Dropdown(
            label="Progress",
            options=[
                ft.dropdown.Option(key=0, text="On-going"),
                ft.dropdown.Option(key=1, text="Solved"),
                ft.dropdown.Option(key=2, text="Unsolved"),
            ],
            value=case.progress,
        )
        date_picker_button = ft.ElevatedButton(
            "Pick Date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=date(2023, 1, 1),
                    last_date=date(2024, 12, 31),
                    on_change=handle_date_change,
                )
            ),
        )
        description_field = ft.TextField(
            label="Description", multiline=True, value=case.description)
        detective_field = ft.TextField(label="Detective", value=case.detective)

        # Submit button
        submit_button = ft.ElevatedButton(
            text="Update Case",
            on_click=button_clicked,
        )

        def go_back(e):
            """Handles the back button click."""
            self.render(self.page)

        # Add the form fields and buttons to the page
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        progress_field,
                        ft.Row([selected_date, date_picker_button],
                               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        description_field,
                        detective_field,
                        submit_button,
                        ft.ElevatedButton(
                            text="Back",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=go_back,
                        ),
                    ],
                    width=700,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=10,
                expand=True,
                alignment=ft.alignment.center,
            )
        )
        self.page.update()
