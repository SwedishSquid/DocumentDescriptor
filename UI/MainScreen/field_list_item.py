from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidgetItem
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtCore import Qt, QEvent, Signal
from UI.MainScreen.field_resizable_qtextedit import FieldTextEdit


class Field(QWidget):
    enterPressed = Signal(QListWidgetItem)

    def __init__(self, caption: str, content: str, name: str,
                 item: QListWidgetItem):
        super().__init__()
        self.name = name
        self._item = item
        self.text_edit = self._create_text_edit(content)

        self.text_edit.textChanged.connect(
            lambda: self._item.setSizeHint(self.sizeHint())
        )
        self.text_edit.resized.connect(
            lambda: self._item.setSizeHint(self.sizeHint())
        )

        self.text_edit.installEventFilter(self)

        layout = QVBoxLayout()
        layout.addWidget(self._create_label(caption))
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def get_content(self):
        return self.text_edit.toPlainText()

    def make_active(self):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.text_edit.setFocus()
        self.text_edit.setTextCursor(cursor)

    def _create_label(self, caption: str):
        label = QLabel(caption)
        label.setMargin(0)
        label.setFont(QFont('Arial', 14))
        return label

    def _create_text_edit(self, content: str):
        text_edit = FieldTextEdit()
        text_edit.setFont(QFont('Arial', 14))
        text_edit.setText(content)

        return text_edit

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.KeyPress and watched is self.text_edit:
            if (event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter)\
                    and self.text_edit.hasFocus():
                self.enterPressed.emit(self._item)
                return True
        return super().eventFilter(watched, event)
