# views/case_view.py
import flet as ft
from controllers.case_controller import CaseController

from routes.destinations import destinations


def on_navigation_change(page: ft.Page, selected_index: int):
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

            def on_tap_down(e: ft.ContainerTapEvent, idx=_idx):
                print("on tap down", idx)

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
        self.page.update()
