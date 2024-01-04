from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QTextEdit, \
    QSizePolicy
from PySide6.QtGui import QFont
from domain.book_data_holders.description_stage import DescriptionStage


class Book(QWidget):
    def __init__(self, number: int, name: str, stage: DescriptionStage):
        super().__init__()

        layout = QHBoxLayout()
        layout.addWidget(self._create_label(str(number)))

        self._text_holder = self._create_text_holder(name)
        layout.addWidget(self._text_holder)

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
        text_edit.setFont(QFont('Arial', 14))
        text_edit.document().setTextWidth(text_edit.viewport().width())
        margins = text_edit.contentsMargins()
        height = text_edit.document().size().height() + margins.top() \
                                                      + margins.bottom()
        text_edit.setFixedHeight(height)
        return text_edit
