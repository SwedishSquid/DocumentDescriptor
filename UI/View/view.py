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
        self.current_book_info = None

        self.qapp = QApplication()
        self.qapp.setWindowIcon(QIcon(str(path_to_pictures.joinpath('file'))))

        self.beginning_window = BeginningWindow(self)
        self.main_window = MainWindow(self)

    def run(self):
        self.beginning_window.show()
        self.qapp.exec()

    def set_project_path(self, path: str):
        if self.app.try_set_project_path(path):
            pass

    def show_main_window(self):
        self.beginning_window.close()
        self.main_window.show()
        # todo: использовать для получения первой книги get_current_book
        #  (позволит начать с того места, где остановились в прошлый раз)
        #  [раньше метода get_current_book не было :)]
        self.current_book_info = self.app.try_set_index_and_get_book(0)
        self._show_book()

    def show_next_book(self):
        self.current_book_info = self.app.get_next_book()
        if self.current_book_info is None:
            quit()
        self._show_book()

    def _show_book(self):
        self.main_window.pdf_viewer.set_document(
            self.current_book_info.absolute_path)
        self._show_book_meta_fields()

    def _show_book_meta_fields(self):
        list_fields = self.main_window.list_fields
        list_fields.clear()
        fields = self.current_book_info.book_meta.fields
        meta_scheme = self.current_book_info.meta_scheme
        for field_name in fields:
            name = meta_scheme.get_human_readable_name(field_name)
            list_fields.add_field(name, fields[field_name], field_name)

    def save_book_meta_as_finished(self):
        list_fields = self.main_window.list_fields
        book_meta = self.current_book_info.book_meta
        for name, content in list_fields.get_all_fields():
            book_meta.fields[name] = content

        self.app.save_as_finished(book_meta)
