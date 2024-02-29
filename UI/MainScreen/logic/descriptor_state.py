from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Slot
from UI.app_state_base import AppStateBase
from UI.MainScreen.main_widget import MainWidget
from UI.descriptor_state_menu_bar import DescriptorStateMenuBar
from pathlib import Path
from app.App import App
from domain.book_data_holders.book_info import BookInfo
from infrastructure.saved_state import SavedStateManager, SavedStateSymbols


class DescriptorState(AppStateBase):
    def __init__(self, window: QMainWindow):
        super(DescriptorState, self).__init__()
        self.main_widget = MainWidget()
        main_widget_fields_font_size = \
            SavedStateManager.get(SavedStateSymbols.FontSize, default_value=14)
        self.main_widget.field_list.change_fields_font_size(
            main_widget_fields_font_size)
        self.main_widget.control_buttons.full_list_button.clicked.connect(
            self._show_full_book_list)
        self.main_widget.control_buttons.continue_button.clicked.connect(
            self._on_saveAndNext_event)
        self.main_widget.Reject_Book_Signal.connect(
            self._on_reject_book_event)
        self.main_widget.New_Book_Index_Chosen_Signal.connect(
            self._on_change_book_via_full_list_event)

        self.window = window
        self.menu_bar = DescriptorStateMenuBar()
        self.menu_bar.increase_font_size.triggered.connect(
            self._on_increase_fields_font_size
        )
        self.menu_bar.decrease_font_size.triggered.connect(
            self._on_decrease_fields_font_size
        )

        self._no_more_files_msg_box = QMessageBox(
            QMessageBox.Icon.Information,
            'Книги закончились!',
            'Документов больше нет. Поздравляем!',
            QMessageBox.StandardButton.Ok
        )
        self._no_more_files_msg_box.setFont(QFont('Arial', 12))

        self.app = App()
        pass

    def get_main_widget(self):
        return self.main_widget

    def transfer_control(self, path: Path):
        # todo: handle this exception
        if not self.app.try_set_project_path(path):
            raise ValueError('by this time project should already exist'
                             ' and be initialised')
        self._show_current_book()
        self.Show_Main_Widget.emit(self.get_main_widget())
        self.window.setMenuBar(self.menu_bar)
        pass

    def _show_next_book(self):
        book_info = self.app.get_next_book()
        if book_info is None:
            self._no_more_files_msg_box.exec()
            return
        self._show_current_book()
        pass

    def _show_book_by_index(self, index: int):
        book_info = self.app.try_set_index_and_get_book(index)
        if book_info is None:
            # todo: handle this situation + log it
            print('index changing was not successive')
        self._show_current_book()
        pass

    def _show_current_book(self):
        book_info = self.app.get_current_book()
        self.main_widget.set_document(
            book_info.absolute_path
        )
        self._set_book_meta_fields(book_info)
        self._set_book_info(book_info)
        pass

    def _set_book_meta_fields(self, book_info: BookInfo):
        field_list = self.main_widget.field_list
        field_list.clear()
        fields = book_info.book_meta.fields
        meta_scheme = book_info.meta_scheme
        for field_name in fields:
            name = meta_scheme.get_human_readable_name(field_name)
            field_list.add_field(name, fields[field_name], field_name)
        pass

    def _set_book_info(self, book_info: BookInfo):
        book_number = self.app.get_book_number(book_info)
        book_name = book_info.book_meta.initial_file_name
        description_stage = self.app.get_book_description_stage(book_info)
        self.main_widget.book_info.set_book(book_number, book_name,
                                            description_stage)

    def _fetch_user_input_to_book_meta(self, book_info: BookInfo):
        field_list = self.main_widget.field_list
        book_meta = book_info.book_meta
        for name, content in field_list.get_all_fields():
            book_meta.fields[name] = content
        pass

    @Slot()
    def _show_full_book_list(self):
        self.main_widget.run_full_book_list_dialog(
            self.app.get_full_book_list()
        )
        pass

    @Slot()
    def _on_saveAndNext_event(self):
        book_info = self.app.get_current_book()
        self._fetch_user_input_to_book_meta(book_info)
        self.app.save_as_finished(book_info.book_meta)
        self._show_next_book()
        pass

    @Slot()
    def _on_reject_book_event(self, message: str):
        book_info = self.app.get_current_book()
        self._fetch_user_input_to_book_meta(book_info)
        self.app.save_as_rejected(book_info.book_meta, message)
        self._show_next_book()
        pass

    @Slot()
    def _on_change_book_via_full_list_event(self, index: int):
        if self.main_widget.field_list.is_changed:
            book_info = self.app.get_current_book()
            self._fetch_user_input_to_book_meta(book_info)
            self.app.save_as_in_progress(book_info.book_meta)
        self._show_book_by_index(index)
    pass

    def _on_increase_fields_font_size(self):
        self.main_widget.field_list.increase_fields_font_size()
        self._save_fields_font_size()
        self.menu_bar.fields_menu.setActiveAction(
            self.menu_bar.increase_font_size)
        self.menu_bar.fields_menu.exec_()

    def _on_decrease_fields_font_size(self):
        self.main_widget.field_list.decrease_fields_font_size()
        self._save_fields_font_size()
        self.menu_bar.fields_menu.setActiveAction(
            self.menu_bar.decrease_font_size)
        self.menu_bar.fields_menu.exec_()

    def _save_fields_font_size(self):
        font_size = self.main_widget.field_list.font_size
        SavedStateManager.put(SavedStateSymbols.FontSize, font_size)
