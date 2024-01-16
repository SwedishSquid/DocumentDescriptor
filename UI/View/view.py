from pathlib import Path

from UI.ManagementScreen.initialized_case_widget import InitializedCaseWidget
from UI.ManagementScreen.not_initialized_case_widget import NotInitializedCaseWidget
from app.App import App
from UI.BeginningScreen.beginning_widget import BeginningWidget
from UI.window_menu_bar import MenuBar
from UI.MainScreen.main_widget import MainWidget
from UI.MainScreen.book_list import BookList
from UI.constant_paths import path_to_pictures
from UI.MainScreen.no_more_files_dialog import NoMoreFilesDialog
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QSizePolicy, QStackedWidget


class View:
    def __init__(self):
        self.chosen_path = None
        self.app = App()
        self.current_book_info = None
        self.current_book_fields_changed = False

        self.q_app = QApplication()
        self.q_app.setWindowIcon(QIcon(str(path_to_pictures.joinpath('file'))))

        self.window = QMainWindow()
        self.window.setMinimumSize(800, 600)
        self.window.setMenuBar(MenuBar())
        self.stacked_widget = QStackedWidget()
        self.window.setCentralWidget(self.stacked_widget)

        self.beginning_widget = BeginningWidget(self)
        self.initialized_case_widget = InitializedCaseWidget(self)
        self.not_initialized_case_widget = NotInitializedCaseWidget(self)
        self.main_widget = MainWidget(self)
        self.stacked_widget.addWidget(self.beginning_widget)
        self.stacked_widget.addWidget(self.not_initialized_case_widget)
        self.stacked_widget.addWidget(self.initialized_case_widget)
        self.stacked_widget.addWidget(self.main_widget)

    def run(self):
        # self.beginning_window.show()
        # self.stacked_widget.addWidget(self.beginning_widget)
        # self.window.setCentralWidget(self.beginning_widget)
        # self.window.showMaximized()
        self.window.show()
        self.q_app.exec()

    # def try_set_project_path(self, path: str):
    #     if self.app.try_set_project_path(path):
    #         self.beginning_widget.show_continue_button()
    #         self.chosen_path = path
    #         return True
    #     self.beginning_widget.hide_continue_button()
    #     return False

    def allow_proceed(self):
        self.beginning_widget.show_continue_button()

    def switch_to_main_widget(self):
        self.app.reset_engine()
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.current_book_info = self.app.get_current_book()
        self._show_book()

    def switch_to_beginning_widget(self):
        self.stacked_widget.setCurrentWidget(self.beginning_widget)
        self.window.setWindowTitle("")

    def switch_to_management_widget_with_path(self, path: str):
        self.chosen_path = Path(path)
        self.window.setWindowTitle(path)
        if self.app.try_set_project_path(self.chosen_path):
            self.initialized_case_widget.reset()
            self.stacked_widget.setCurrentWidget(self.initialized_case_widget)
        else:
            self.stacked_widget.setCurrentWidget(self.not_initialized_case_widget)

    def init_project(self):
        self.app.glue.init_project(self.current_book_info)
        self.initialized_case_widget.reset()
        self.stacked_widget.setCurrentWidget(self.initialized_case_widget)

    def resume_preprocessing(self):
        self.app.glue.get_preprocessor_generator()

    def show_next_book(self):
        self.current_book_info = self.app.get_next_book()
        self.current_book_fields_changed = False
        if self.current_book_info is None:
            NoMoreFilesDialog().exec()
            return
        self._show_book()

    def show_book_by_number(self, num: int):
        self.current_book_info = self.app.try_set_index_and_get_book(num)
        self._show_book()

    def _show_book(self):
        self.main_widget.set_document(
            self.current_book_info.absolute_path)
        self._show_book_meta_fields()

    def _show_book_meta_fields(self):
        field_list = self.main_widget.field_list
        field_list.clear()
        fields = self.current_book_info.book_meta.fields
        meta_scheme = self.current_book_info.meta_scheme
        for field_name in fields:
            name = meta_scheme.get_human_readable_name(field_name)
            field_list.add_field(name, fields[field_name], field_name)

    def _save_fields_to_book_meta(self):
        field_list = self.main_widget.field_list
        book_meta = self.current_book_info.book_meta
        for name, content in field_list.get_all_fields():
            book_meta.fields[name] = content

    def save_book_meta_as_rejected(self, message: str):
        self._save_fields_to_book_meta()
        self.app.save_as_rejected(self.current_book_info.book_meta, message)

    def save_book_meta_as_finished(self):
        self._save_fields_to_book_meta()
        self.app.save_as_finished(self.current_book_info.book_meta)

    def save_book_meta_as_in_progress(self):
        if not self.current_book_fields_changed:
            return
        self._save_fields_to_book_meta()
        self.app.save_as_in_progress(self.current_book_info.book_meta)

    def show_full_book_list(self, book_list: BookList):
        book_list.clear()
        book_records = self.app.get_full_book_list()
        for i in range(len(book_records)):
            book_list.add_book(
                i,
                str(book_records[i].rel_path.name),
                book_records[i].descr_stage
            )

    def on_fields_change(self):
        self.current_book_fields_changed = True
