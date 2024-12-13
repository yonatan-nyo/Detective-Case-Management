import flet as ft
from src.routes.destinations import destinations
from src.controllers.case_controller import CaseController


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
        from src.views.schedule_view import Schedule
        Schedule().render(page)
    elif selected_index == 4:
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


class Statistic:
    def __init__(self):
        self.case_controller = CaseController()

    def _create_bar_chart(self, top_entities, title, color):
        """Creates a bar chart for the given entities."""
        if not top_entities:
            return ft.Text("No data available", size=16)

        bar_groups = []
        bottom_axis_labels = []

        for i, entity in enumerate(top_entities):
            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=entity.cases_count,
                            width=40,
                            color=color,
                            tooltip=f"{entity.name}: {entity.cases_count} cases",
                            border_radius=0,
                        ),
                    ],
                )
            )
            bottom_axis_labels.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Container(
                        ft.Text(entity.name, size=8,
                                text_align=ft.TextAlign.CENTER),
                        padding=2
                    )
                )
            )

        max_y = max([e.cases_count for e in top_entities]) + \
            5 if top_entities else 10

        return ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.Colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=30,
                title=ft.Text(f"Number of {title} Cases", size=10),
                title_size=30
            ),
            bottom_axis=ft.ChartAxis(
                labels=bottom_axis_labels,
                labels_size=30,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_300,
                width=1,
                dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
            max_y=max_y,
            interactive=True,
            height=300,
            width=600,
        )

    def render(self, page: ft.Page):
        rail = ft.NavigationRail(
            selected_index=4,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=-0.9,
            destinations=destinations,
            on_change=lambda e: on_navigation_change(
                page, e.control.selected_index),
        )

        top_victims = self.case_controller.get_top_ten_victims()
        top_suspects = self.case_controller.get_top_ten_suspects()

        victims_chart = self._create_bar_chart(
            top_victims,
            "Victims",
            ft.Colors.BLUE
        )

        suspects_chart = self._create_bar_chart(
            top_suspects,
            "Suspects",
            ft.Colors.RED
        )

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Row(
                    [
                        rail,
                        ft.VerticalDivider(width=1),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Case Statistics", size=20,
                                            weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        "Top 10 Victims by Case Involvement", size=14),
                                    victims_chart,
                                    ft.Text(
                                        "Top 10 Suspects by Case Involvement", size=14),
                                    suspects_chart
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True,
                            ),
                            padding=10,
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
                bgcolor="#111518",
                expand=True
            )
        )
        page.update()
