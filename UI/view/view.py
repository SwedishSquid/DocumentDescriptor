from app.App import App
from domain.book_data_holders.book_info import BookInfo
from UI.BeginningScreen.beginning_window import BeginningWindow
from UI.MainScreen.main_window import MainWindow
from UI.constant_paths import path_to_pictures
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication


class View:
    def __init__(self):
        self.app = App()

        self.qapp = QApplication()
        self.qapp.setWindowIcon(QIcon(str(path_to_pictures.joinpath('file'))))

        self.beginning_window = BeginningWindow(self.set_project_path, self.show_main_window)
        self.main_window = MainWindow()

    def run(self):
        self.beginning_window.show()
        self.qapp.exec()

    def set_project_path(self, path: str):
        if self.app.try_set_project_path(path):
            pass

    def show_main_window(self):
        self.beginning_window.close()
        self.main_window.show()
        self.show_book(self.app.try_set_index_and_get_book(0))

    def show_book(self, book_info: BookInfo):
        self.main_window.pdf_viewer.set_document(book_info.absolute_path)

    def show_next_book(self):

        self.show_book(self.app.get_next_book())

