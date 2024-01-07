from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QFont
from domain.book_data_holders.description_stage import DescriptionStage
from UI.resizable_qtextedit import ResizableTextEdit


class Book(QWidget):
    def __init__(self, number: int, name: str, stage: DescriptionStage):
        super().__init__()
        self.number = number

        layout = QHBoxLayout()
        layout.addWidget(self._create_label())

        self._text_holder = self._create_text_holder(name)
        layout.addWidget(self._text_holder)
        layout.setSpacing(10)

        self.setLayout(layout)

    def _create_label(self):
        label = QLabel(str(self.number))
        label.setFont(QFont('Arial', 14))
        return label

    def _create_text_holder(self, content: str):
        text_edit = ResizableTextEdit()
        text_edit.setFont(QFont('Arial', 14))
        text_edit.setText(content)
        text_edit.setReadOnly(True)
        text_edit.setDisabled(True)
        return text_edit
