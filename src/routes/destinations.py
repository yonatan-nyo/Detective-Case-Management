import flet as ft

selected_index = 0

destinations = [
    ft.NavigationRailDestination(
        icon=ft.Icons.PERSON_OUTLINED,
        selected_icon=ft.Icon(ft.Icons.PERSON),
        label="Manajemen Kasus"
    ),
    ft.NavigationRailDestination(
        icon=ft.Icons.PERSON_OUTLINED,
        selected_icon=ft.Icon(ft.Icons.PERSON),
        label="Manajemen Suspect",
    ),
    ft.NavigationRailDestination(
        icon=ft.Icons.PERSON_OUTLINED,
        selected_icon=ft.Icon(ft.Icons.PERSON),
        label_content=ft.Text("Manajemen Victim"),
    ),
    ft.NavigationRailDestination(
        icon=ft.Icons.DATE_RANGE_OUTLINED,
        selected_icon=ft.Icon(ft.Icons.DATE_RANGE),
        label_content=ft.Text("Schedule"),
    ),
    ft.NavigationRailDestination(
        icon=ft.Icons.SIGNAL_CELLULAR_0_BAR_OUTLINED,
        selected_icon=ft.Icon(ft.Icons.SIGNAL_CELLULAR_0_BAR),
        label_content=ft.Text("Statistik"),
    ),
]
