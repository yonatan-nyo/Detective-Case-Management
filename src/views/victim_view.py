import os
import shutil
import uuid
from datetime import datetime
import flet as ft
from controllers.victim_controller import VictimController
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
        from views.suspect_view import SuspectView
        SuspectView().render(page)
    elif selected_index == 2:
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


class VictimView:
    def __init__(self):
        self.controller = VictimController()
        self.page = None
        self.page_number = 1
        self.per_page = 12
        self.total_pages = 1  # Initialize total pages

    def fetch_victims(self):
        """Fetches victims for the current page."""
        victims = self.controller.get_all_victims()
        self.total_pages = (len(victims) + self.per_page - 1) // self.per_page
        start_idx = (self.page_number - 1) * self.per_page
        end_idx = start_idx + self.per_page
        return victims[start_idx:end_idx]

    def build_victims_component(self, victims):
        """Builds the victims component with the given list of victims."""
        temp_row = []
        for _idx, victim in enumerate(victims):
            def on_hover(e):
                e.control.bgcolor = "black" if e.data == "true" else ft.Colors.BLACK54
                e.control.update()

            def on_tap_down(_e: ft.ContainerTapEvent, idx=_idx):
                self.render_victim_detail(victims[idx].id)

            victim_card = (
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"NIK: {victim.nik}", size=12),
                            ft.Text(f"Name: {victim.name}", size=14),
                            ft.Text(f"Age: {victim.age}", size=12),
                            ft.Text(
                                f"Forensic Result: {victim.forensic_result}", size=12),
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
                    victim_card,
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
        """Renders the victim management view."""
        self.page = page
        victims = self.fetch_victims()

        rail = ft.NavigationRail(
            selected_index=2,
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
                                content=ft.Text("Victim Management", size=24),
                                padding=10,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                [self.build_victims_component(victims)],
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

        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, on_click=lambda e: self.render_add_victim()
        )

        self.page.update()

    def render_add_victim(self):
        """Renders the Add Victim form with unique filenames for uploaded pictures."""
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
            """Handles form submission for adding a victim."""
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

            forensic_result = forensic_result_field.value.strip()
            if not forensic_result:
                forensic_result_field.error_text = "Forensic result is required."
                self.page.update()
                return

            # Add the victim via the controller
            self.controller.add_victim(
                nik, picture_path, name, age, forensic_result)

            # After submission, go back to victim management view
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
        forensic_result_field = ft.TextField(label="Forensic Result")

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
            text="Add Victim", on_click=handle_form_submission
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
                        forensic_result_field,
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

    def render_victim_detail(self, victim_id):
        """Renders the details of a specific victim."""
        victim = self.controller.get_victim_by_id(victim_id)
        if not victim:
            self.page.controls.clear()
            self.page.add(
                ft.Container(
                    content=ft.Text(
                        f"No victim found with ID {victim_id}.",
                        size=16,
                        color=ft.Colors.RED,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
            self.page.update()
            return

        # Build the victim detail view
        detail_view = ft.Column(
            [
                ft.Text("Victim Details", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"NIK: {victim.nik}", size=18),
                ft.Text(f"Name: {victim.name}", size=18),
                ft.Text(f"Age: {victim.age}", size=18),
                ft.Text(f"Forensic Result: {victim.forensic_result}", size=18),
                ft.Text(f"Cases: {', '.join([str(case.id) for case in victim.cases])}"
                        if victim.cases else "Cases: None", size=18),
                ft.Image(
                    src=victim.picture_path,
                    width=300,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                ) if victim.picture_path and os.path.exists(victim.picture_path)
                else ft.Text("No Picture Available", size=16),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Back to List",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: self.render(self.page),
                        ),
                        ft.ElevatedButton(
                            "Edit Victim",
                            icon=ft.Icons.EDIT,
                            on_click=lambda _: self.render_edit_victim(
                                victim_id),
                        ),
                        ft.ElevatedButton(
                            "Delete Victim",
                            icon=ft.Icons.DELETE,
                            bgcolor=ft.Colors.RED,
                            on_click=lambda _: self.delete_victim(victim_id),
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

    def render_edit_victim(self, victim_id):
        """Renders the Edit Victim form."""
        victim = self.controller.get_victim_by_id(victim_id)
        if not victim:
            self.page.controls.clear()
            self.page.add(
                ft.Container(
                    content=ft.Text(
                        f"No victim found with ID {victim_id}.",
                        size=16,
                        color=ft.Colors.RED,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
            self.page.update()
            return

        # Prepopulate fields with victim data
        nik_field = ft.TextField(label="NIK", value=victim.nik)
        picture_path_field = ft.TextField(
            label="Picture Path", value=victim.picture_path, read_only=True
        )
        name_field = ft.TextField(label="Name", value=victim.name)
        age_field = ft.TextField(
            label="Age", value=str(victim.age), keyboard_type=ft.KeyboardType.NUMBER
        )
        forensic_result_field = ft.TextField(
            label="Forensic Result", value=victim.forensic_result)

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
            forensic_result = forensic_result_field.value.strip()
            picture_path = picture_path_field.value.strip()

            if not nik or not name or not age or not forensic_result:
                # Validate inputs and display errors
                if not nik:
                    nik_field.error_text = "NIK is required."
                if not name:
                    name_field.error_text = "Name is required."
                if not age:
                    age_field.error_text = "Age is required."
                if not forensic_result:
                    forensic_result_field.error_text = "Forensic result is required."
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

            # Update the victim details
            self.controller.update_victim(
                victim_id, nik=nik, picture_path=picture_path, name=name, age=age, forensic_result=forensic_result
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
                        forensic_result_field,
                        ft.ElevatedButton("Update Victim",
                                          on_click=handle_update),
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

    def delete_victim(self, victim_id):
        """Deletes a victim after confirmation."""
        def confirm_delete(_):
            """Handles the confirmation dialog response."""
            self.controller.delete_victim(victim_id)
            self.render(self.page)
            self.page.close(dlg_modal)

        def cancel_delete(_):
            """Closes the confirmation dialog without deleting."""
            self.page.close(dlg_modal)

        # Confirmation dialog
        dlg_modal = ft.AlertDialog(
            title=ft.Text("Confirm Deletion"),
            content=ft.Text(
                "Are you sure you want to delete this victim? This action cannot be undone."),
            actions=[
                ft.ElevatedButton(
                    "Yes", on_click=confirm_delete, bgcolor=ft.Colors.RED),
                ft.ElevatedButton("Cancel", on_click=cancel_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dlg_modal)
        self.page.update()
