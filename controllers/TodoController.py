from models.database import SessionLocal
from models.Todo import Todo


class TodoController:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_todos(self):
        return self.db.query(Todo).all()

    def add_todo(self, text):
        new_todo = Todo(text=text, completed=False)
        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)

    def delete_todo(self, todo_id):
        todo = self.db.query(Todo).filter(Todo.id == todo_id).first()
        if todo:
            self.db.delete(todo)
            self.db.commit()

    def complete_todo(self, todo_id):
        todo = self.db.query(Todo).filter(Todo.id == todo_id).first()
        if todo:
            todo.completed = True
            self.db.commit()
