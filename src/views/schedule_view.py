import flet as ft
from routes.destinations import destinations
from datetime import datetime, timedelta
import calendar

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
        CaseView().render(page)
    elif selected_index == 1:
        from views.suspect_view import SuspectView
        SuspectView().render(page)
    elif selected_index == 2:
        from views.victim_view import VictimView
        VictimView().render(page)
    elif selected_index == 3:
        from views.schedule_view import Schedule
        from datetime import datetime, timedelta
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

class Schedule:
    def __init__(self):
        self.current_month = 5
        self.current_year = 2024
        
    def render(self, page):
        """Renders the schedule."""
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
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        content=self.create_page(),
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )
        self.page.update()

    
    def create_page(self):
            header = ft.Row(
                [
                    ft.Dropdown(
                        label="Bulan",
                        options=[
                            ft.dropdown.Option("Januari"),
                            ft.dropdown.Option("Februari"),
                            ft.dropdown.Option("Maret"),
                            ft.dropdown.Option("April"),
                            ft.dropdown.Option("Mei"),
                            ft.dropdown.Option("Juni"),
                            ft.dropdown.Option("Juli"),
                            ft.dropdown.Option("Agustus"),
                            ft.dropdown.Option("September"),
                            ft.dropdown.Option("Oktober"),
                            ft.dropdown.Option("November"),
                            ft.dropdown.Option("Desember"),
                        ],
                        value="Mei",
                        width=120,
                        on_change=lambda e: self.update_date(e.control.value, self.current_year),
                    ),
                    ft.Dropdown(
                        label="Tahun",
                        options=[
                            ft.dropdown.Option("2023"),
                            ft.dropdown.Option("2024"),
                            ft.dropdown.Option("2025"),
                        ],
                        value="2024",
                        width=100,
                        on_change=lambda e: self.update_date(self.current_month, e.control.value),
                    ),
                    ft.Dropdown(
                        label="Prioritas",
                        options=[
                            ft.dropdown.Option("Semua"),
                            ft.dropdown.Option("Tinggi"),
                            ft.dropdown.Option("Sedang"),
                            ft.dropdown.Option("Rendah"),
                        ],
                        value="Semua",
                        width=120,
                    ),
                    ft.Dropdown(
                        label="Victim",
                        options=[
                            ft.dropdown.Option("Budi"),
                            ft.dropdown.Option("Siti"),
                            ft.dropdown.Option("Andi"),
                        ],
                        value="Budi",
                        width=100,
                    ),
                    ft.Dropdown(
                        label="Suspect",
                        options=[
                            ft.dropdown.Option("Budi"),
                            ft.dropdown.Option("Siti"),
                            ft.dropdown.Option("Andi"),
                        ],
                        value="Budi",
                        width=100,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=15,
            )

            calendar_days = []
            # Get the current month and year from the dropdowns

            days_in_month = calendar.monthrange(self.current_year, self.current_month)[1]
            first_day_of_month = datetime(self.current_year, self.current_month, 1)
            start_day = first_day_of_month - timedelta(days=first_day_of_month.weekday() + 1)

            for i in range(42):
                day = start_day + timedelta(days=i)
                calendar_days.append(
                ft.Container(
                    content=ft.Text(
                    str(day.day),
                    color=ft.colors.WHITE if day.month == self.current_month else ft.colors.GREY,
                    size=14,
                    ),
                    bgcolor=ft.colors.BLACK26 if day.month == self.current_month else ft.colors.BLACK12,
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

            content = ft.Column(
                [
                    ft.Text(
                        "SCHEDULE",
                        size=25,
                        weight="bold",
                        color=ft.colors.BLACK,
                    ),
                    header,
                    ft.Divider(color=ft.colors.GREY),
                    calendar_grid,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
                expand=True,
            )

            return content
        
    def update_date(self, month, year):
        """Updates the current month and year."""
        month_mapping = {
            "Januari": 1,
            "Februari": 2,
            "Maret": 3,
            "April": 4,
            "Mei": 5,
            "Juni": 6,
            "Juli": 7,
            "Agustus": 8,
            "September": 9,
            "Oktober": 10,
            "November": 11,
            "Desember": 12,
        }
        self.current_month = month_mapping.get(month, self.current_month)
        self.current_year = int(year)
        # Re-render the page with updated values
        self.render(self.page)