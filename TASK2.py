from abc import ABC, abstractmethod
from typing import List


# 1. Базовый интерфейс для команд
class Action(ABC):
    @abstractmethod
    def execute(self):
        """Выполнить действие."""
        pass

    @abstractmethod
    def rollback(self):
        """Отменить действие."""
        pass

class GraphicObject:
    def __init__(self, object_type: str):
        self.object_type = object_type

    def create(self):
        print(f"Создана графическая фигура: {self.object_type}.")

    def relocate(self, x: int, y: int):
        print(f"Фигура {self.object_type} перемещена в позицию ({x}, {y}).")

    def remove(self):
        print(f"Фигура {self.object_type} удалена.")

class AddObject(Action):
    def __init__(self, obj: GraphicObject):
        self.obj = obj

    def execute(self):
        self.obj.create()

    def rollback(self):
        self.obj.remove()


class MoveObject(Action):
    def __init__(self, obj: GraphicObject, new_x: int, new_y: int):
        self.obj = obj
        self.new_x = new_x
        self.new_y = new_y
        self.previous_x = 0
        self.previous_y = 0

    def execute(self):
        self.previous_x, self.previous_y = self.new_x, self.new_y
        self.obj.relocate(self.new_x, self.new_y)

    def rollback(self):
        self.obj.relocate(self.previous_x, self.previous_y)


class DeleteObject(Action):
    def __init__(self, obj: GraphicObject):
        self.obj = obj

    def execute(self):
        self.obj.remove()

    def rollback(self):
        self.obj.create()

class ActionHistory:
    def __init__(self):
        self.done_actions: List[Action] = []
        self.redo_stack: List[Action] = []

    def add_action(self, action: Action):
        self.done_actions.append(action)
        self.redo_stack.clear()

    def undo_last(self):
        if self.done_actions:
            last_action = self.done_actions.pop()
            last_action.rollback()
            self.redo_stack.append(last_action)
        else:
            print("Нет действий для отмены.")

    def redo_last(self):
        if self.redo_stack:
            action_to_redo = self.redo_stack.pop()
            action_to_redo.execute()
            self.done_actions.append(action_to_redo)
        else:
            print("Нет действий для повтора.")

class DrawingEditor:
    def __init__(self):
        self.history = ActionHistory()

    def apply_action(self, action: Action):
        action.execute()
        self.history.add_action(action)

    def undo(self):
        print("\nОтмена последнего действия:")
        self.history.undo_last()

    def redo(self):
        print("\nПовтор последнего действия:")
        self.history.redo_last()



if __name__ == "__main__":

    circle = GraphicObject("Круг")
    square = GraphicObject("Квадрат")
    add_circle = AddObject(circle)
    move_circle = MoveObject(circle, 15, 30)
    delete_square = DeleteObject(square)
    add_square = AddObject(square)
    editor = DrawingEditor()
    editor.apply_action(add_circle)
    editor.apply_action(move_circle)
    editor.apply_action(delete_square)
    editor.apply_action(add_square)

    editor.undo()
    editor.redo()
