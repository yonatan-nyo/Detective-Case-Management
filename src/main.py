from models.init_database import init_db
import flet as ft

from views.case_view import CaseView
from views.suspect_view import SuspectView
from views.victim_view import VictimView


def main(page: ft.Page):
    page.title = "Kasus Kriminal"
    CaseView().render(page)


# def on_navigation_change(page: ft.Page, selected_index: int):
#     """Handles navigation change to display appropriate content."""
#     # if selected_index == 0:  # Manajemen Kasus
#     rail = ft.NavigationRail(
#         selected_index=selected_index,
#         label_type=ft.NavigationRailLabelType.ALL,
#         min_width=100,
#         min_extended_width=400,
#         group_alignment=-0.9,
#         destinations=route.destinations,
#         on_change=lambda e: on_navigation_change(
#             page, e.control.selected_index),
#     )
#     page.controls.clear()
#     if selected_index == 0:
#         page.add(
#             ft.Row(
#                 [
#                     rail,
#                     ft.VerticalDivider(width=1),
#                     CaseView().build(),  # Display the case management view
#                 ],
#                 expand=True,
#             )
#         )
#     elif selected_index == 1:
#         page.add(
#             ft.Row(
#                 [
#                     rail,
#                     ft.VerticalDivider(width=1),
#                     SuspectView().build(page),  # Display the suspect management view
#                 ],
#                 expand=True,
#             )
#         )
#     elif selected_index == 2:
#         page.add(
#             ft.Row(
#                 [
#                     rail,
#                     ft.VerticalDivider(width=1),
#                     VictimView().build(page),  # Display the victim management view
#                 ],
#                 expand=True,
#             )
#         )
#     page.update()


if __name__ == "__main__":
    init_db()
    ft.app(main)
