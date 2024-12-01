import sys
from PyQt6.QtWidgets import QApplication
from views.MainWindow import MainWindow
from models.database import init_db


def main():
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
