from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidgetItem, QSizePolicy
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtCore import Qt, QEvent, Signal
from UI.MainScreen.field_resizable_qtextedit import FieldTextEdit


class Field(QWidget):
    enterPressed = Signal(QListWidgetItem)

    def __init__(self,
                 caption: str,
                 content: str,
                 name: str,
                 font_size: int,
                 item: QListWidgetItem):

        super().__init__()
        self.name = name
        self._item = item
        self.text_edit = self._create_text_edit(content, font_size)

        self.text_edit.textChanged.connect(
            lambda: self._item.setSizeHint(self.sizeHint())
        )
        self.text_edit.resized.connect(
            lambda: self._item.setSizeHint(self.sizeHint())
        )

        self.text_edit.installEventFilter(self)

        self._caption_label = self._create_caption_label(caption, font_size)
        layout = QVBoxLayout()
        layout.addWidget(self._caption_label)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def get_content(self):
        return self.text_edit.toPlainText().replace('\n', ' ')

    def make_active(self):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.text_edit.setFocus()
        self.text_edit.setTextCursor(cursor)

    def change_font_size(self, new_size: int):
        label_font = self._caption_label.font()
        label_font.setPointSize(new_size)
        self._caption_label.setFont(label_font)
        text_edit_font = self.text_edit.font()
        text_edit_font.setPointSize(new_size)
        self.text_edit.setFont(text_edit_font)
        self.text_edit.textChanged.emit()

    def _create_caption_label(self, caption: str, font_size: int):
        label = QLabel(caption)
        label.setFont(QFont('Arial', font_size))
        label.setMargin(0)
        label.setFont(QFont('Arial', 14))
        return label

    def _create_text_edit(self, content: str, font_size: int):
        text_edit = FieldTextEdit()
        text_edit.setFont(QFont('Arial', font_size))
        text_edit.setText(content)

        return text_edit

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.KeyPress and watched is self.text_edit:
            if (event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter)\
                    and self.text_edit.hasFocus():
                self.enterPressed.emit(self._item)
                return True
        return super().eventFilter(watched, event)
