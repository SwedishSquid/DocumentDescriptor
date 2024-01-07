from PySide6.QtWidgets import QDialog, QVBoxLayout
from UI.MainScreen.book_list import BookList


class FullBookList(QDialog):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.setWindowTitle("Полный список книг")
        self.resize(800, 600)

        self.book_list = BookList(view, self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.book_list)
        # self.accepted.connect(self.view.save_book_meta_as_in_progress)

    def run(self):
        self.exec()
