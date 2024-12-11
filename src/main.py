import flet as ft

from models.init_database import init_db
from views.case_view import CaseView


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Kasus Kriminal"
    CaseView().render(page)


if __name__ == "__main__":
    init_db()
    ft.app(main)
