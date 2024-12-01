from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QImage
from controllers.TodoController import TodoController

tick = QImage('assets/tick.png')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('views/mainwindow.ui', self)

        self.controller = TodoController()
        self.model = QStandardItemModel()
        self.todoView.setModel(self.model)

        self.load_todos()

        self.addButton.pressed.connect(self.add_todo)
        self.deleteButton.pressed.connect(self.delete_todo)
        self.completeButton.pressed.connect(self.complete_todo)

    def load_todos(self):
        self.model.clear()
        todos = self.controller.get_all_todos()
        for todo in todos:
            item = QStandardItem(todo.text)
            # Store the `id` as metadata
            item.setData(todo.id, Qt.ItemDataRole.UserRole)
            if todo.completed:
                item.setData(tick, Qt.ItemDataRole.DecorationRole)
            self.model.appendRow(item)

    def add_todo(self):
        text = self.todoEdit.text()
        if text:
            self.controller.add_todo(text)
            self.todoEdit.setText("")
            self.load_todos()

    def delete_todo(self):
        selected = self.todoView.selectedIndexes()
        if selected:
            item = self.model.itemFromIndex(selected[0])
            todo_id = item.data(Qt.ItemDataRole.UserRole)
            self.controller.delete_todo(todo_id)
            self.load_todos()

    def complete_todo(self):
        selected = self.todoView.selectedIndexes()
        if selected:
            item = self.model.itemFromIndex(selected[0])
            todo_id = item.data(Qt.ItemDataRole.UserRole)
            self.controller.complete_todo(todo_id)
            self.load_todos()
