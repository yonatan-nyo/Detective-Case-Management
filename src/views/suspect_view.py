
import os
import shutil
import uuid
from datetime import datetime

import flet as ft
from src.controllers.suspect_controller import SuspectController
from src.routes.destinations import destinations


def on_navigation_change(page: ft.Page, selected_index: int):
    """Handles navigation change to display appropriate content."""
    page.floating_action_button = None
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

            suspect_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                # Picture of the suspect
                                ft.Container(
                                    content=ft.Image(
                                        src=suspect.picture_path,  # Assuming the path is valid
                                        width=80,
                                        height=80,
                                        fit=ft.ImageFit.COVER,
                                    ),
                                    border_radius=5,
                                    bgcolor=ft.Colors.GREY_800,
                                    margin=2,
                                ),
                                # Suspect details
                                ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "NIK: ", weight=ft.FontWeight.BOLD),
                                                ft.Text(suspect.nik),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "Name: ", weight=ft.FontWeight.BOLD),
                                                ft.Text(suspect.name),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "Age: ", weight=ft.FontWeight.BOLD),
                                                ft.Text(str(suspect.age)),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "Gender: ", weight=ft.FontWeight.BOLD),
                                                ft.Text(
                                                    "Male" if suspect.gender else "Female"),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),

                                    ],
                                    spacing=2,
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=6,
                        ),
                        ft.Container(
                            content=ft.Text(
                                f"Note: {suspect.note}",
                                max_lines=3,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                style=ft.TextStyle(
                                    size=12, color=ft.Colors.GREY_400),
                            ),
                        ),
                    ]),
                border_radius=8,
                bgcolor=ft.Colors.BLACK54,
                padding=10,
                on_hover=on_hover,
                on_tap_down=lambda e, idx=_idx: on_tap_down(e, idx),
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

        search_results = ft.Column(
            [self.build_suspects_component(suspects)], expand=True)

        def perform_search(e):
            name = name_field.value.strip()
            nik = nik_field.value.strip()

            if not name and not nik:
                page.snack_bar = ft.SnackBar(content=ft.Text(
                    "Please enter Name or NIK to search."))
                page.snack_bar.open = True
                page.update()
                return

            search_results.controls.clear()

            # Perform search via the controller
            results = self.controller.search_suspects(name, nik)

            if results:
                search_results.controls.append(
                    self.build_suspects_component(results))
            else:
                search_results.controls.append(
                    ft.Text("No suspects found matching your criteria."))
            # Update page with search results
            page.update()

        def clear_search(e):
            name_field.value = ""
            nik_field.value = ""
            self.render(page)

        name_field = ft.TextField(label="Search by Name", width=300)
        nik_field = ft.TextField(label="Search by NIK", width=300)
        search_button = ft.ElevatedButton("Search", on_click=perform_search)
        clear_button = ft.ElevatedButton("Clear", on_click=clear_search)

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
                                        "Suspect Management", size=24),
                                    padding=10,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Row([name_field, nik_field, search_button,
                                        clear_button], alignment=ft.MainAxisAlignment.START),
                                search_results,
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
                            [picture_path_field, file_picker_button],
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
                bgcolor="#111518",
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
                    f"Cases: {', '.join([str(case.id) for case in suspect.cases])}"
                    if suspect.cases else "Cases: None",
                    size=18
                ),
                ft.Text(f"Note: {suspect.note or 'N/A'}", size=18),
                ft.Image(
                    src=suspect.picture_path,
                    width=300,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                ) if suspect.picture_path and os.path.exists(suspect.picture_path)
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
                bgcolor="#111518",
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
        picture_path_field = ft.TextField(
            label="Picture Path", value=suspect.picture_path, read_only=True
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
                picture_path_field.value = destination_path
                picture_path_field.update()

        pick_file_dialog = ft.FilePicker(on_result=pick_file_result)

        def handle_update(e):
            """Handles the update process."""
            nik = nik_field.value.strip()
            name = name_field.value.strip()
            age = age_field.value
            gender = gender_dropdown.value
            note = note_field.value.strip()
            picture_path = picture_path_field.value.strip()

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
                suspect_id, nik=nik, picture_path=picture_path, name=name, age=age, gender=gender, note=note
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
                            [picture_path_field, ft.ElevatedButton(
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
                bgcolor="#111518",
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
