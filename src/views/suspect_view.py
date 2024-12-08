
import os
import shutil
import uuid
from datetime import datetime

import flet as ft
from controllers.suspect_controller import SuspectController
from routes.destinations import destinations


def on_navigation_change(page: ft.Page, selected_index: int):
    page.floating_action_button = None
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
    elif selected_index == 3:
        from views.schedule_view import Schedule
        Schedule().render(page)
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
                self.render_suspect_detail(suspects[idx].id)

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
                picturePath_field.value = destination_path
                picturePath_field.update()
            else:
                picturePath_field.value = "No file selected"
                picturePath_field.update()

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

            picturePath = picturePath_field.value.strip()
            if not os.path.exists(picturePath):
                picturePath_field.error_text = "Invalid picture path."
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
                nik, picturePath, name, age, gender, note
            )

            # After submission, go back to suspect management view
            self.render(self.page)

        # Form fields
        nik_field = ft.TextField(label="NIK")
        picturePath_field = ft.TextField(
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

        def go_back(e):
            """Handles the back button click."""
            self.render(self.page)

        # Layout and render the form
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        nik_field,
                        ft.Row(
                            [picturePath_field, file_picker_button],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        name_field,
                        age_field,
                        gender_dropdown,
                        note_field,
                        submit_button,
                        ft.ElevatedButton(
                            text="Back",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=go_back,
                        ),
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

    def render_suspect_detail(self, suspect_id):
        """Renders the details of a specific suspect by ID."""
        # Fetch the suspect by ID
        suspect = self.controller.get_suspect_by_id(suspect_id)
        if not suspect:
            # If no suspect is found, show an error message
            self.page.controls.clear()
            self.page.add(
                ft.Container(
                    content=ft.Text(
                        f"No suspect found with ID {suspect_id}.",
                        size=16,
                        color=ft.Colors.RED,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
            self.page.update()
            return

        # Build the suspect detail view
        detail_view = ft.Column(
            [
                ft.Text("Suspect Details", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"NIK: {suspect.nik}", size=18),
                ft.Text(f"Name: {suspect.name}", size=18),
                ft.Text(f"Age: {suspect.age}", size=18),
                ft.Text(
                    f"Gender: {'Male' if suspect.gender else 'Female'}", size=18
                ),
                ft.Text(
                    f"Cases: {', '.join([str(case.id) for case in suspect.cases])}" if suspect.cases else "Cases: None",
                    size=18
                ),
                ft.Text(f"Note: {suspect.note or 'N/A'}", size=18),
                ft.Image(
                    src=suspect.picturePath,
                    width=300,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                ) if suspect.picturePath and os.path.exists(suspect.picturePath)
                else ft.Text("No Picture Available", size=16),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Back to List",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.render(self.page),
                        ),
                        ft.ElevatedButton(
                            "Edit Suspect",
                            icon=ft.Icons.EDIT,
                            on_click=lambda _: self.render_edit_suspect(
                                suspect_id),
                        ),
                        ft.ElevatedButton(
                            "Delete Suspect",
                            icon=ft.Icons.DELETE,
                            bgcolor=ft.Colors.RED,
                            on_click=lambda _: self.delete_suspect(suspect_id),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )

        # Clear the page and add the detail view
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=detail_view,
                padding=20,
                expand=True,
                alignment=ft.alignment.center,
            )
        )
        self.page.update()

    def render_edit_suspect(self, suspect_id):
        """Renders the Edit Suspect form."""
        suspect = self.controller.get_suspect_by_id(suspect_id)
        if not suspect:
            self.page.controls.clear()
            self.page.add(
                ft.Container(
                    content=ft.Text(
                        f"No suspect found with ID {suspect_id}.",
                        size=16,
                        color=ft.Colors.RED,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
            self.page.update()
            return

        # Prepopulate fields with suspect data
        nik_field = ft.TextField(label="NIK", value=suspect.nik)
        picturePath_field = ft.TextField(
            label="Picture Path", value=suspect.picturePath, read_only=True
        )
        name_field = ft.TextField(label="Name", value=suspect.name)
        age_field = ft.TextField(
            label="Age", value=str(suspect.age), keyboard_type=ft.KeyboardType.NUMBER
        )
        gender_dropdown = ft.Dropdown(
            label="Gender",
            value=suspect.gender,
            options=[
                ft.dropdown.Option(key=True, text="Male"),
                ft.dropdown.Option(key=False, text="Female"),
            ],
        )
        note_field = ft.TextField(
            label="Note (Optional)", value=suspect.note, multiline=True)

        def pick_file_result(e: ft.FilePickerResultEvent):
            """Handle file picker result."""
            if e.files:
                file = e.files[0]
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                unique_filename = f"{timestamp}_{uuid.uuid4().hex}_{file.name}"
                destination_path = os.path.join("img/", unique_filename)
                shutil.copy(file.path, destination_path)
                picturePath_field.value = destination_path
                picturePath_field.update()

        pick_file_dialog = ft.FilePicker(on_result=pick_file_result)

        def handle_update(e):
            """Handles the update process."""
            nik = nik_field.value.strip()
            name = name_field.value.strip()
            age = age_field.value
            gender = gender_dropdown.value
            note = note_field.value.strip()
            picturePath = picturePath_field.value.strip()

            if not nik or not name or not age or gender is None:
                # Validate inputs and display errors
                if not nik:
                    nik_field.error_text = "NIK is required."
                if not name:
                    name_field.error_text = "Name is required."
                if not age:
                    age_field.error_text = "Age is required."
                if gender is None:
                    gender_dropdown.error_text = "Gender is required."
                self.page.update()
                return

            try:
                age = int(age)
                if age <= 0:
                    raise ValueError
            except ValueError:
                age_field.error_text = "Age must be a positive number."
                self.page.update()
                return

            # Update the suspect details
            self.controller.update_suspect(
                suspect_id, nik=nik, picturePath=picturePath, name=name, age=age, gender=gender, note=note
            )
            self.render(self.page)

        # Add file picker overlay
        self.page.overlay.append(pick_file_dialog)

        def go_back(e):
            """Handles the back button click."""
            self.render(self.page)

        # Layout for the form
        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        nik_field,
                        ft.Row(
                            [picturePath_field, ft.ElevatedButton(
                                "Pick Picture", on_click=lambda _: pick_file_dialog.pick_files(allow_multiple=False))],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        name_field,
                        age_field,
                        gender_dropdown,
                        note_field,
                        ft.ElevatedButton("Update Suspect",
                                          on_click=handle_update),
                        ft.ElevatedButton(
                            text="Back",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=go_back,
                        )
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

    def delete_suspect(self, suspect_id):
        """Deletes a suspect after confirmation."""
        def confirm_delete(_):
            """Handles the confirmation dialog response."""
            self.controller.delete_suspect(suspect_id)
            self.render(self.page)
            self.page.close(dlg_modal)

        def cancel_delete(_):
            """Closes the confirmation dialog without deleting."""
            self.page.close(dlg_modal)

        # Confirmation dialog
        dlg_modal = ft.AlertDialog(
            title=ft.Text("Confirm Deletion"),
            content=ft.Text(
                "Are you sure you want to delete this suspect? This action cannot be undone."),
            actions=[
                ft.ElevatedButton(
                    "Yes", on_click=confirm_delete, bgcolor=ft.Colors.RED),
                ft.ElevatedButton("Cancel", on_click=cancel_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dlg_modal)
        self.page.update()
