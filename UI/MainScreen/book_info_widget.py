from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from domain.book_data_holders.description_stage import DescriptionStage
import UI.colors as colors


class BookInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.book_number_label = QLabel()
        self.book_number_label.setFont(QFont("Arial", 10))

        self.name_holder = self._create_name_holder()

        self.setAutoFillBackground(True)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.book_number_label)
        self.layout().addWidget(self.name_holder)

    def set_book(self, number: int, name: str, stage: DescriptionStage):
        self.book_number_label.setText(str(number))
        self.name_holder.setText(name)

        palette = self.name_holder.viewport().palette()
        palette.setColor(self.name_holder.viewport().backgroundRole(),
                         colors.color_by_stage_for_text_document_background[
                             stage])
        self.name_holder.viewport().setPalette(palette)

        palette = self.palette()
        palette.setColor(self.backgroundRole(),
                         colors.color_by_stage_for_widget_background[stage])
        self.setPalette(palette)

    def _create_name_holder(self):
        name_holder = QTextEdit()
        name_holder.setCurrentFont(QFont("Arial", 10))
        name_holder.setReadOnly(True)
        name_holder.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        name_holder.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        name_holder.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        height = name_holder.fontMetrics().height() \
                 + 2 * name_holder.document().documentMargin() + 1
        name_holder.setFixedHeight(height)
        return name_holder
