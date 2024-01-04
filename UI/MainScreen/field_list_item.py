from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtGui import QFont


class Field(QWidget):
    def __init__(self, caption: str, content: str, name: str):
        super().__init__()
        self.name = name
        self._line_edit = self._create_line_edit(content)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self._create_label(caption), 1)
        layout.addWidget(self._line_edit, 5)

        self.setLayout(layout)

    def get_content(self):
        return self._line_edit.text()

    def _create_label(self, caption: str):
        label = QLabel(caption)
        label.setMargin(10)
        label.setFont(QFont('Arial', 14))
        return label

    def _create_line_edit(self, content: str):
        line_edit = QLineEdit()
        line_edit.setText(content)
        line_edit.setMinimumHeight(50)
        line_edit.setFrame(True)
        line_edit.setFont(QFont('Arial', 14))

        return line_edit
