from UI.app_state_base import AppStateBase
from UI.MainScreen.main_widget import MainWidget
from pathlib import Path
from app.App import App
from PySide6.QtCore import Slot
from domain.book_data_holders.book_info import BookInfo
from UI.MainScreen.no_more_files_dialog import NoMoreFilesDialog


class DescriptorState(AppStateBase):
    def __init__(self):
        super(DescriptorState, self).__init__()
        self.main_widget = MainWidget()
        self.main_widget.control_buttons.full_list_button.clicked.connect(
            self._show_full_book_list)
        self.main_widget.control_buttons.continue_button.clicked.connect(
            self._on_saveAndNext_event)
        self.main_widget.Reject_Book_Signal.connect(
            self._on_reject_book_event)
        self.main_widget.New_Book_Index_Chosen_Signal.connect(
            self._on_change_book_via_full_list_event)

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
        pass

    def _show_next_book(self):
        book_info = self.app.get_next_book()
        if book_info is None:
            NoMoreFilesDialog().exec()
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
        book_info = self.app.get_current_book()
        # todo: change save type to something that depends on previous state
        self._fetch_user_input_to_book_meta(book_info)
        self.app.save_with_previous_state_flag(book_info.book_meta)
        self._show_book_by_index(index)
    pass
