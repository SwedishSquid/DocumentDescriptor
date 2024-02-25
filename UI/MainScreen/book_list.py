from PySide6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView,\
    QDialog
from PySide6.QtCore import Qt, Signal
from UI.MainScreen.book_list_item import Book
from domain.book_data_holders.description_stage import DescriptionStage
import UI.colors as colors


class BookList(QListWidget):
    Book_Index_Chosen_Signal = Signal(int)

    def __init__(self, dialog: QDialog):
        super().__init__()
        self.dialog = dialog

        self.itemClicked.connect(self._on_book_click)
        self.itemClicked.connect(lambda: dialog.done(1))

        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(10)
        self.setSpacing(3)

    def add_book(self, number: int, book_name: str, stage: DescriptionStage):
        item = QListWidgetItem()
        book = Book(number, book_name, stage)

        self.addItem(item)
        self.setItemWidget(item, book)

        item.setSizeHint(book.sizeHint())
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        item.setBackground(colors.color_by_stage_for_widget_background[stage])
        pass

    def _on_book_click(self, item: QListWidgetItem):
        book = self.itemWidget(item)
        self.Book_Index_Chosen_Signal.emit(book.number)
