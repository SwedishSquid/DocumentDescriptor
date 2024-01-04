from PySide6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from UI.MainScreen.book_list_item import Book
from domain.book_data_holders.description_stage import DescriptionStage
from PySide6.QtCore import Qt
from PySide6.QtGui import QColorConstants


class BookList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(5)
        self.setSpacing(3)

    def add_book(self, book_name: str, stage: DescriptionStage):
        item = QListWidgetItem()
        widget = Book(self.count() + 1, book_name, stage)

        item.setSizeHint(widget.sizeHint())
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        item.setBackground(QColorConstants.Gray)
        self.addItem(item)
        self.setItemWidget(item, widget)
