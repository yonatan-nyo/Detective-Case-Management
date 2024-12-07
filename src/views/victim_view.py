import flet as ft
from controllers.victim_controller import VictimController
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
        from views.suspect_view import SuspectView
        SuspectView().render(page)
    elif selected_index == 2:
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

            def on_tap_down(e: ft.ContainerTapEvent, idx=_idx):
                print("Victim tapped:", idx)

            victim_card = (
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"NIK: {victim.nik}", size=12),
                            ft.Text(f"Name: {victim.name}", size=14),
                            ft.Text(f"Age: {victim.age}", size=12),
                            ft.Text(
                                f"Forensic Result: {victim.forensicResult}", size=12),
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

    def previous_page(self, e):
        """Handles the Previous button click."""
        if self.page_number > 1:
            self.page_number -= 1
            self.render(self.page)

    def next_page(self, e):
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
        self.page.update()
