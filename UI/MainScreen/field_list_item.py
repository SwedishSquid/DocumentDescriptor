from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidgetItem
from PySide6.QtGui import QFont
from UI.resizable_qtextedit import ResizableTextEdit


class Field(QWidget):
    view = None

    def __init__(self, caption: str, content: str, name: str,
                 item: QListWidgetItem):
        super().__init__()
        self.name = name
        self._item = item
        self._text_edit = self._create_text_edit(content)

        self._text_edit.textChanged.connect(
            lambda: self._item.setSizeHint(self.sizeHint())
        )
        self._text_edit.textChanged.connect(self.view.on_fields_change)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self._create_label(caption), 1)
        layout.addWidget(self._text_edit, 5)

        self.setLayout(layout)

    def get_content(self):
        return self._text_edit.toPlainText()

    def _create_label(self, caption: str):
        label = QLabel(caption)
        label.setMargin(10)
        label.setFont(QFont('Arial', 14))
        return label

    def _create_text_edit(self, content: str):
        text_edit = ResizableTextEdit()
        text_edit.setFont(QFont('Arial', 14))
        text_edit.setText(content)

        return text_edit
