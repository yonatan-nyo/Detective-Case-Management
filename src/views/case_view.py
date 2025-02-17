# views/case_view.py
from datetime import date
import flet as ft
from fpdf import FPDF

from src.controllers.case_controller import CaseController
from src.routes.destinations import destinations


def on_navigation_change(page: ft.Page, selected_index: int):
    """Handles navigation change to display appropriate content."""
    page.floating_action_button = None
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
        from src.views.suspect_view import SuspectView
        SuspectView().render(page)
    elif selected_index == 2:
        from src.views.victim_view import VictimView
        VictimView().render(page)
    elif selected_index == 3:
        from src.views.schedule_view import Schedule
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


class CaseView:
    def __init__(self):
        self.controller = CaseController()
        self.page = None
        self.page_number = 1
        self.per_page = 12
        self.total_pages = 1  # Initialize total pages
        self.filter_progress = None

    def fetch_cases(self):
        """Fetches cases for the current page with optional filtering."""
        pagination_data = self.controller.get_all_cases_pagination(
            page=self.page_number,
            per_page=self.per_page,
            filter_progress=self.filter_progress,  # Pass the filter
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
                            ft.Text(
                                f"Start Date: {str(case.startDate).split(' ')[0]}", size=12),
                            ft.Text(f"Detective: {case.detective}", size=12),
                            ft.Text(f"Priority: {case.priority}", size=12),
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

    def build_dropdown(self):
        """Builds the dropdown for filtering cases."""
        def dropdown_changed(e):
            filter_mapping = {
                "All": None,
                "Solved": 0,
                "Unsolved": 1,
                "Ongoing": 2,
            }
            self.filter_progress = filter_mapping.get(dd.value, None)
            self.page_number = 1  # Reset to the first page
            self.render(self.page)  # Re-render with the updated filter

        # Map current filter progress to dropdown value
        filter_mapping_reverse = {
            None: "All",
            0: "Solved",
            1: "Unsolved",
            2: "Ongoing",
        }
        current_filter = filter_mapping_reverse.get(
            self.filter_progress, "Remove Filter")

        # Define the dropdown
        dd = ft.Dropdown(
            label="Progress",
            width=150,
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("Solved"),
                ft.dropdown.Option("Unsolved"),
                ft.dropdown.Option("Ongoing"),
            ],
            value=current_filter,  # Set the current value
            on_change=dropdown_changed,  # Attach the event handler
        )

        return dd

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
            ft.Container(
                content=ft.Row(
                    [
                        rail,
                        ft.VerticalDivider(width=1),
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        "Case Management", size=24),
                                    padding=10,
                                    alignment=ft.alignment.center,
                                ),
                                self.build_dropdown(),
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
                ),
                bgcolor="#111518",
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
            priority = priority_field.value

            # Validate description
            if not description.strip():
                description_field.error_text = "Description cannot be empty."
                self.page.update()
                return

            # Add the new case using the controller
            self.controller.add_case(
                progress, start_date, description, detective, priority)

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
        priority_field = ft.Dropdown(
            label="Priority",
            options=[
                ft.dropdown.Option(key="Rendah", text="Rendah"),
                ft.dropdown.Option(key="Sedang", text="Sedang"),
                ft.dropdown.Option(key="Tinggi", text="Tinggi"),
            ],
        )

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
                        priority_field,
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
                bgcolor="#111518",
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
                    bgcolor="#111518",
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

        def assign_suspects(e):
            """Handles the assign suspects button click."""
            self.render_assign_suspects(case)

        def assign_victims(e):
            """Handles the assign victims button click."""
            self.render_assign_victims(case)

        def download_report(e):
            """Handles the download report button click."""
            case = self.controller.get_case_by_id(case_id)
            if case:
                # Buat dialog untuk memilih lokasi penyimpanan
                file_picker = ft.FilePicker(
                    on_result=lambda e: handle_file_pick(e, case)
                )
                self.page.overlay.append(file_picker)
                self.page.update()
                file_picker.save_file(
                    dialog_title="Simpan Laporan Kasus",
                    file_name=f"laporan_kasus_{case_id}.pdf"
                )

        def handle_file_pick(e, case):
            """Proses generate PDF setelah memilih lokasi"""
            if e.path:
                try:
                    generate_case_report(case, e.path)
                    self.page.show_snack_bar(
                        ft.SnackBar(content=ft.Text(
                            "Laporan berhasil dibuat!"))
                    )
                except Exception as ex:
                    self.page.show_snack_bar(
                        ft.SnackBar(content=ft.Text(
                            f"Gagal membuat laporan: {str(ex)}"))
                    )

        def generate_case_report(case, filename):
            """Generates a PDF report for the given case."""
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Judul
            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(0, 10, "Laporan Kasus", ln=True, align="C")
            pdf.ln(10)

            # Informasi Kasus
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, "Informasi Kasus", ln=True)

            pdf.set_font("Arial", size=12)
            case_details = [
                ("Case ID", str(case.id)),
                ("Progress", case.progress),
                ("Start Date", str(case.startDate).split(' ')[0]),
                ("Detective", case.detective if case.detective else "-"),
                ("Priority", case.priority if case.priority else "-")
            ]

            # Menambahkan detail kasus
            for label, value in case_details:
                pdf.cell(60, 10, f"{label}:", 0, 0)
                pdf.cell(0, 10, str(value), ln=True)

            # Deskripsi Kasus
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Deskripsi Kasus", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, case.description)

            # Tersangka
            if case.suspects:
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "Daftar Tersangka", ln=True)
                pdf.set_font("Arial", size=12)
                for suspect in case.suspects:
                    pdf.cell(0, 10, f"- {suspect.name}", ln=True)

            # Korban
            if case.victims:
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "Daftar Korban", ln=True)
                pdf.set_font("Arial", size=12)
                for victim in case.victims:
                    pdf.cell(0, 10, f"- {victim.name}", ln=True)

            # Menyimpan PDF
            pdf.output(filename)

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
                                ft.Text(str(case.startDate).split(
                                    ' ')[0], size=16),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Text("Detective:", size=16, weight="bold"),
                                ft.Text("-", size=16)
                                if case.detective is None
                                else ft.Text(case.detective, size=16)
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Text("Priority:", size=16, weight="bold"),
                                ft.Text("-", size=16)
                                if case.priority is None
                                else ft.Text(case.priority, size=16)
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Text("Suspects:", size=16, weight="bold"),
                                ft.Text(
                                    "No suspects assigned.", size=16)
                                if not case.suspects
                                else ft.Text(
                                    ", ".join([suspect.name for suspect in case.suspects]), size=16
                                )
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Text("Victims:", size=16, weight="bold"),
                                ft.Text("No victim assigned.", size=16)
                                if not case.victims
                                else ft.Text(
                                    ", ".join([victim.name for victim in case.victims]), size=16
                                )
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
                                ft.ElevatedButton(
                                    text="Assign Suspects",
                                    icon=ft.Icons.PERSON_ADD,
                                    on_click=assign_suspects,
                                ),
                                ft.ElevatedButton(
                                    text="Assign Victims",
                                    icon=ft.Icons.PERSON_ADD,
                                    on_click=assign_victims,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.ElevatedButton(
                            text="Back",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=go_back,
                        ),
                        ft.ElevatedButton(
                            text="Download Report",
                            icon=ft.Icons.DOWNLOAD,
                            on_click=download_report,
                        ),
                    ],
                    expand=True,
                ),
                padding=20,
                alignment=ft.alignment.center,
                bgcolor="#111518",
            ),
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
            priority = priority_field.value

            # Validate description
            if not description.strip():
                description_field.error_text = "Description cannot be empty."
                self.page.update()
                return

            # Update the case using the controller
            self.controller.update_case(
                case.id, progress, start_date, description, detective, priority
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
        priority_field = ft.Dropdown(
            label="Priority",
            options=[
                ft.dropdown.Option(key="Rendah", text="Rendah"),
                ft.dropdown.Option(key="Sedang", text="Sedang"),
                ft.dropdown.Option(key="Tinggi", text="Tinggi"),
            ],
            value=case.priority,
        )

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
                        priority_field,
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
                bgcolor="#111518",
            ),
        )
        self.page.update()

    def render_assign_suspects(self, case):
        """Renders a dialog to assign suspects to the case."""
        # Fetch unassigned suspects
        case_id = case.id
        unassigned_suspects = self.controller.get_unassigned_suspects(case_id)

        # Create a dropdown for unassigned suspects
        suspect_dropdown = ft.Dropdown(
            label="Select Suspect",
            options=[
                ft.dropdown.Option(key=suspect.id, text=suspect.name)
                for suspect in unassigned_suspects
            ]
        )

        def assign_suspect(e):
            if suspect_dropdown.value:
                self.controller.assign_suspect_to_case(
                    case.id, int(suspect_dropdown.value))
                # Re-render the case detail view
                self.render_detail(case.id)

        assign_button = ft.ElevatedButton(
            text="Assign Suspect",
            on_click=assign_suspect
        )

        # Show list of currently assigned suspects
        assigned_suspects_list = ft.Column(
            [
                ft.Row([
                    ft.Text(suspect.name, size=16),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, s=suspect: self.remove_suspect_from_case(
                            case, s)
                    )
                ])
                for suspect in case.suspects
            ]
        )

        # Add the dialog to the page
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Assign Suspects to Case", size=24),
                    ft.Text(f"Case ID: {case.id}", size=16),
                    ft.Row([suspect_dropdown, assign_button]),
                    ft.Text("Currently Assigned Suspects:",
                            size=18, weight="bold"),
                    assigned_suspects_list,
                    ft.ElevatedButton(
                        text="Back",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.render_detail(case.id)
                    )
                ]),
                padding=20,
                alignment=ft.alignment.center,
                bgcolor="#111518",
            )
        )
        self.page.update()

    def remove_suspect_from_case(self, case, suspect):
        """Remove a suspect from the case."""
        self.controller.remove_suspect_from_case(case.id, suspect.id)
        # Re-render the assign suspects view
        self.render_assign_suspects(case)

    def render_assign_victims(self, case):
        """Renders a dialog to assign victims to the case."""
        # Fetch unassigned victims
        case_id = case.id
        unassigned_victims = self.controller.get_unassigned_victims(case_id)

        # Create a dropdown for unassigned victims
        victim_dropdown = ft.Dropdown(
            label="Select Victim",
            options=[
                ft.dropdown.Option(key=victim.id, text=victim.name)
                for victim in unassigned_victims
            ]
        )

        def assign_victim(e):
            if victim_dropdown.value:
                self.controller.assign_victim_to_case(
                    case.id, int(victim_dropdown.value))
                # Re-render the case detail view
                self.render_detail(case.id)

        assign_button = ft.ElevatedButton(
            text="Assign Victim",
            on_click=assign_victim
        )

        # Show list of currently assigned victims
        assigned_victims_list = ft.Column(
            [
                ft.Row([
                    ft.Text(victim.name, size=16),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, s=victim: self.remove_victim_from_case(
                            case, s)
                    )
                ])
                for victim in case.victims
            ]
        )

        # Add the dialog to the page
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Assign Victims to Case", size=24),
                    ft.Text(f"Case ID: {case.id}", size=16),
                    ft.Row([victim_dropdown, assign_button]),
                    ft.Text("Currently Assigned Victims:",
                            size=18, weight="bold"),
                    assigned_victims_list,
                    ft.ElevatedButton(
                        text="Back",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.render_detail(case.id)
                    )
                ]),
                padding=20,
                alignment=ft.alignment.center,
                bgcolor="#111518",
            )
        )
        self.page.update()

    def remove_victim_from_case(self, case, victim):
        """Remove a victim from the case."""
        self.controller.remove_victim_from_case(case.id, victim.id)
        # Re-render the assign victims view
        self.render_assign_victims(case)
