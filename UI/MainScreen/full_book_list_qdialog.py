from PySide6.QtWidgets import QDialog, QVBoxLayout
from UI.MainScreen.book_list import BookList


class FullBookList(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Полный список книг")
        self.resize(800, 600)

        self.book_list = BookList()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.book_list)

    def run(self):
        self.exec()
