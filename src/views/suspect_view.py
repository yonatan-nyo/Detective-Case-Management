
import os
import shutil
import uuid
from datetime import datetime

import flet as ft
from controllers.suspect_controller import SuspectController
from routes.destinations import destinations


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
        from views.case_view import CaseView
        CaseView().render(page)
    elif selected_index == 1:
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


class SuspectView:
    def __init__(self):
        self.controller = SuspectController()
        self.page = None
        self.page_number = 1
        self.per_page = 12
        self.total_pages = 1  # Initialize total pages

    def fetch_suspects(self):
        """Fetch suspects for the current page."""
        suspects = self.controller.get_all_suspects()
        self.total_pages = (len(suspects) + self.per_page - 1) // self.per_page
        start_idx = (self.page_number - 1) * self.per_page
        end_idx = start_idx + self.per_page
        return suspects[start_idx:end_idx]

    def build_suspects_component(self, suspects):
        """Build the suspects component with the given list of suspects."""
        temp_row = []
        for _idx, suspect in enumerate(suspects):
            def on_hover(e):
                e.control.bgcolor = "black" if e.data == "true" else ft.Colors.BLACK54
                e.control.update()

            def on_tap_down(_e: ft.ContainerTapEvent, idx=_idx):
                print("Suspect tapped:", idx)

            suspect_card = (
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"NIK: {suspect.nik}", size=12),
                            ft.Text(f"Name: {suspect.name}", size=14),
                            ft.Text(f"Age: {suspect.age}", size=12),
                            ft.Text(
                                f"Gender: {'Male' if suspect.gender else 'Female'}", size=12),
                            ft.Text(f"Note: {suspect.note}", size=12),
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
                    suspect_card,
                    padding=5,
                    col={"sm": 6, "md": 4, "xl": 3},
                )
            )

        return ft.ResponsiveRow(temp_row, expand=False)

    def build_pagination_controls(self):
        """Build pagination controls."""
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
        """Renders the suspect management view."""
        self.page = page
        suspects = self.fetch_suspects()

        rail = ft.NavigationRail(
            selected_index=1,
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
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Text("Suspect Management", size=24),
                                padding=10,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                [self.build_suspects_component(suspects)],
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

        # Add FAB for adding a suspect
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, on_click=lambda e: self.render_add_suspect()
        )
        self.page.update()

    def render_add_suspect(self):
        """Renders the Add Suspect form with unique filenames for uploaded pictures."""
        # Directory to upload files
        upload_directory = "img/"

        # Ensure the upload directory exists
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        # File picker logic
        def pick_file_result(e: ft.FilePickerResultEvent):
            """Handles the file picker result."""
            if e.files:
                # Use the first selected file
                file = e.files[0]

                # Generate a unique filename
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                unique_filename = f"{timestamp}_{uuid.uuid4().hex}_{file.name}"
                destination_path = os.path.join(
                    upload_directory, unique_filename)

                # Copy the file to the upload directory
                shutil.copy(file.path, destination_path)

                # Update the picture path field
                picture_path_field.value = destination_path
                picture_path_field.update()
            else:
                picture_path_field.value = "No file selected"
                picture_path_field.update()

        pick_file_dialog = ft.FilePicker(on_result=pick_file_result)

        # Form submission logic
        def handle_form_submission(e):
            """Handles form submission for adding a suspect."""
            # Validate and retrieve input values
            nik = nik_field.value.strip()
            if not nik:
                nik_field.error_text = "NIK is required."
                self.page.update()
                return

            picture_path = picture_path_field.value.strip()
            if not os.path.exists(picture_path):
                picture_path_field.error_text = "Invalid picture path."
                self.page.update()
                return

            name = name_field.value.strip()
            if not name:
                name_field.error_text = "Name is required."
                self.page.update()
                return

            try:
                age = int(age_field.value)
                if age <= 0:
                    raise ValueError
            except ValueError:
                age_field.error_text = "Age must be a positive number."
                self.page.update()
                return

            gender = gender_dropdown.value
            if gender is None:
                gender_dropdown.error_text = "Gender is required."
                self.page.update()
                return

            note = note_field.value.strip()

            # Add the suspect via the controller
            self.controller.add_suspect(
                nik, picture_path, name, age, gender, note
            )

            # After submission, go back to suspect management view
            self.render(self.page)

        # Form fields
        nik_field = ft.TextField(label="NIK")
        picture_path_field = ft.TextField(
            label="Picture Path", read_only=True, hint_text="Select a picture"
        )
        name_field = ft.TextField(label="Name")
        age_field = ft.TextField(
            label="Age", keyboard_type=ft.KeyboardType.NUMBER
        )
        gender_dropdown = ft.Dropdown(
            label="Gender",
            options=[
                ft.dropdown.Option(key=True, text="Male"),
                ft.dropdown.Option(key=False, text="Female"),
            ],
        )
        note_field = ft.TextField(label="Note (Optional)", multiline=True)

        # File picker button
        file_picker_button = ft.ElevatedButton(
            "Pick Picture",
            icon=ft.Icons.IMAGE,
            on_click=lambda _: pick_file_dialog.pick_files(
                allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"]
            )
        )

        # Submit button
        submit_button = ft.ElevatedButton(
            text="Add Suspect", on_click=handle_form_submission
        )

        # Add file picker to page overlay
        self.page.overlay.append(pick_file_dialog)

        # Layout and render the form
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        nik_field,
                        ft.Row(
                            [picture_path_field, file_picker_button],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        name_field,
                        age_field,
                        gender_dropdown,
                        note_field,
                        submit_button,
                    ],
                    expand=True,
                    width=700,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=10,
                expand=True,
                alignment=ft.alignment.center,
            )
        )
        self.page.update()
