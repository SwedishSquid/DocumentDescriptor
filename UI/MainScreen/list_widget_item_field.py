from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit,\
    QSizePolicy, QLayout
from PySide6.QtGui import QFont, QPalette, QColorConstants


class Field(QWidget):
    def __init__(self, caption: str):
        super().__init__()

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self._create_label(caption), 1)
        line_edit = QLineEdit()
        line_edit.setMinimumHeight(50)
        line_edit.setFrame(True)
        line_edit.setFont(QFont('Arial', 14))
        layout.addWidget(line_edit, 5)
        self.setFixedHeight(120)

        self.setLayout(layout)

    def _create_label(self, caption: str):
        label = QLabel(caption)
        label.setMargin(10)
        label.setFont(QFont('Arial', 14))
        return label
