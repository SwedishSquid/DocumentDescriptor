from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QTextEdit
from PySide6.QtGui import QFont
from domain.book_data_holders.description_stage import DescriptionStage


class Book(QWidget):
    def __init__(self, number: int, name: str, stage: DescriptionStage):
        super().__init__()

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self._create_label(str(number)), 1)
        layout.addWidget(self._create_text_holder(name), 5)

        self.setFixedHeight(120)
        self.setLayout(layout)

    def _create_label(self, caption: str):
        label = QLabel(caption)
        label.setMargin(10)
        label.setFont(QFont('Arial', 14))
        return label

    def _create_text_holder(self, content: str):
        text_edit = QTextEdit()
        text_edit.setText(content)
        text_edit.setReadOnly(True)
        return text_edit
