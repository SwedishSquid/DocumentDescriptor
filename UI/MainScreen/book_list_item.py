from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QFont, QColorConstants
from domain.book_data_holders.description_stage import DescriptionStage
from UI.resizable_qtextedit import ResizableTextEdit
import UI.colors as colors


class Book(QWidget):
    def __init__(self, number: int, name: str, stage: DescriptionStage):
        super().__init__()
        self.number = number
        self._stage = stage

        layout = QHBoxLayout()
        layout.addWidget(self._create_label_with_number())

        self._name_holder = self._create_name_holder(name)
        layout.addWidget(self._name_holder)

        self.setLayout(layout)

    def _create_label_with_number(self):
        label = QLabel(str(self.number + 1))
        label.setFont(QFont('Arial', 14))
        return label

    def _create_name_holder(self, content: str):
        text_edit = ResizableTextEdit()
        text_edit.setFont(QFont('Arial', 14))
        text_edit.setTextColor(QColorConstants.Black)
        text_edit.setText(content)
        text_edit.setReadOnly(True)
        text_edit.setDisabled(True)

        palette = text_edit.viewport().palette()
        palette.setColor(text_edit.viewport().backgroundRole(),
                         colors.color_by_stage_for_text_document_background[
                             self._stage])
        text_edit.viewport().setPalette(palette)
        return text_edit

