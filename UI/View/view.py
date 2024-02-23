from pathlib import Path
from UI.ManagementScreen.initialized_case_widget import InitializedCaseWidget
from UI.ManagementScreen.not_initialized_case_widget import NotInitializedCaseWidget
from app.App import App
from UI.BeginningScreen.beginning_widget import BeginningWidget
from UI.window_menu_bar import MenuBar
from UI.main_widget_menu_bar import MainWidgetMenuBar
from UI.MainScreen.main_widget import MainWidget
from UI.constant_paths import path_to_pictures
from UI.MainScreen.no_more_files_dialog import NoMoreFilesDialog
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QSizePolicy, QStackedWidget
from PySide6.QtCore import Signal, Slot


class View:
    def __init__(self):
        # self.chosen_path = None
        self.app = App()
        self.current_book_info = None

        self.q_app = QApplication()
        self.q_app.setWindowIcon(QIcon(str(path_to_pictures.joinpath('file'))))

        self.window = QMainWindow()
        self.window.setWindowTitle("Document descriptor")
        self.window.setMinimumSize(800, 600)
        self.window.setMenuBar(MenuBar())   # todo: add functionality to menu bar or remove it
        self.stacked_widget = QStackedWidget()
        self.window.setCentralWidget(self.stacked_widget)

        self.beginning_widget = BeginningWidget()
        self.beginning_widget.Proceed_Button_Signal.connect(self._on_project_path_chosen_event)

        self.main_widget = MainWidget()
        self.main_widget.control_buttons.full_list_button.clicked.connect(self.show_full_book_list)
        self.main_widget.control_buttons.continue_button.clicked.connect(self.on_saveAndNext_event)
        self.main_widget.Reject_Book_Signal.connect(self.on_reject_book_event)
        self.main_widget.New_Book_Index_Chosen_Signal.connect(self.on_change_book_via_full_list_event)
        self.main_widget_menu_bar = MainWidgetMenuBar()
        self.main_widget_menu_bar.increase_font_size.triggered.connect(self.main_widget.increase_fields_font_size)
        self.main_widget_menu_bar.decrease_font_size.triggered.connect(self.main_widget.decrease_fields_font_size)

        self.stacked_widget.addWidget(self.beginning_widget)

        # fixme: unify under one widget with recognizable name
        self.initialized_case_widget = InitializedCaseWidget(self)
        self.not_initialized_case_widget = NotInitializedCaseWidget(self)
        self.stacked_widget.addWidget(self.not_initialized_case_widget)
        self.stacked_widget.addWidget(self.initialized_case_widget)

        self.stacked_widget.addWidget(self.main_widget)

    def run(self):
        self.stacked_widget.setCurrentWidget(self.beginning_widget)
        self.window.show()
        self.q_app.exec()

    def switch_to_main_widget(self):
        self.app.reset_engine()
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.window.setMenuBar(self.main_widget_menu_bar)
        self.current_book_info = self.app.get_current_book()
        self._show_book()

    def switch_to_beginning_widget(self):
        self.stacked_widget.setCurrentWidget(self.beginning_widget)
        self.window.setWindowTitle("")
        pass

    @Slot()
    def _on_project_path_chosen_event(self, path: Path):
        self.switch_to_management_widget_with_path(str(path))
        pass

    def switch_to_management_widget_with_path(self, path: str):
        # todo: simplify
        chosen_path = Path(path)
        self.window.setWindowTitle(path)
        if self.app.try_set_project_path(chosen_path):
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
        next_book_info = self.app.get_next_book()
        if next_book_info is None:
            NoMoreFilesDialog().exec()
            return
        self.current_book_info = next_book_info
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
        field_list.is_change = False

    def save_book_meta_as_rejected(self, message: str):
        self._save_fields_to_book_meta()
        self.app.save_as_rejected(self.current_book_info.book_meta, message)

    def save_book_meta_as_finished(self):
        self._save_fields_to_book_meta()
        self.app.save_as_finished(self.current_book_info.book_meta)

    def save_book_meta_as_in_progress(self):
        self._save_fields_to_book_meta()
        self.app.save_as_in_progress(self.current_book_info.book_meta)

    @Slot()
    def show_full_book_list(self):
        self.main_widget.run_full_book_list_dialog(self.app.get_full_book_list())
        pass

    @Slot()
    def on_reject_book_event(self, message: str):
        self.save_book_meta_as_rejected(message)
        self.show_next_book()
        pass

    @Slot()
    def on_saveAndNext_event(self):
        self.save_book_meta_as_finished()
        self.show_next_book()
        pass

    @Slot()
    def on_change_book_via_full_list_event(self, index: int):
        if self.main_widget.field_list.is_change:
            self.save_book_meta_as_in_progress()

        self.show_book_by_number(index)
        pass
