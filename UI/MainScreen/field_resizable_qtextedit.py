from UI.resizable_qtextedit import ResizableTextEdit
from PySide6.QtCore import Signal


class FieldTextEdit(ResizableTextEdit):
    resized = Signal()

    def __init__(self):
        super().__init__()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit()
