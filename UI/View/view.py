from app.App import App
from UI.BeginningScreen.beginning_window import BeginningWindow
from UI.MainScreen.main_window import MainWindow
from UI.MainScreen.book_list import BookList
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

    def try_set_project_path(self, path: str):
        if self.app.try_set_project_path(path):
            self.beginning_window.show_continue_button()
            return True
        self.beginning_window.hide_continue_button()
        return False


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
        self.app.save_as_in_progress(self.current_book_info.book_meta)
        self._show_book()

    def _show_book(self):
        self.main_window.pdf_viewer.set_document(
            self.current_book_info.absolute_path)
        self._show_book_meta_fields()

    def _show_book_meta_fields(self):
        field_list = self.main_window.field_list
        field_list.clear()
        fields = self.current_book_info.book_meta.fields
        meta_scheme = self.current_book_info.meta_scheme
        for field_name in fields:
            name = meta_scheme.get_human_readable_name(field_name)
            field_list.add_field(name, fields[field_name], field_name)

    def _save_fields_to_book_meta(self):
        field_list = self.main_window.field_list
        book_meta = self.current_book_info.book_meta
        for name, content in field_list.get_all_fields():
            book_meta.fields[name] = content

    def save_book_meta_as_finished(self):
        self._save_fields_to_book_meta()
        self.app.save_as_finished(self.current_book_info.book_meta)

    def save_book_meta_as_rejected(self):
        self._save_fields_to_book_meta()
        self.app.save_as_rejected(self.current_book_info.book_meta)

    def show_full_book_list(self, book_list: BookList):
        book_list.clear()
        for book_record in self.app.get_full_book_list():
            book_list.add_book(
                str(book_record.rel_path.name), book_record.descr_stage)
