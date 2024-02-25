from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy
from UI.MainScreen.control_buttons import ControlButtons
from UI.MainScreen.reject_qdialog import Reject
from UI.MainScreen.full_book_list_qdialog import FullBookList
from UI.MainScreen.field_list import FieldList
from UI.MainScreen.browser_pdf_viewer import BrowserPdfViewer
from UI.MainScreen.book_info_widget import BookInfoWidget
from pathlib import Path


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_viewer = BrowserPdfViewer()
        self.pdf_viewer.set_file(Path())
        self.field_list = FieldList(font_size=14)
        self.control_buttons = ControlButtons()  # part of public interface
        self.book_info = BookInfoWidget()

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self._create_left_widget(), 1)
        layout.addWidget(self.pdf_viewer, 1)
        self.setLayout(layout)

        self._reject_dialog = Reject()
        self.Reject_Book_Signal = self._reject_dialog.Reject_Book_Signal
        self.control_buttons.reject_button.clicked.connect(self._reject_dialog.run)

        self._full_book_list_dialog = FullBookList()
        self.New_Book_Index_Chosen_Signal =\
            self._full_book_list_dialog.book_list.Book_Index_Chosen_Signal
        pass

    def run_full_book_list_dialog(self, full_list_records: list):
        """full_list_records: list[FullBookRecord] from engine"""
        self._full_book_list_dialog.run_dialog(full_list_records)
        pass

    def _create_left_widget(self):
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.field_list, 20)
        layout.addWidget(self.control_buttons, 4)
        layout.addWidget(self.book_info, 1)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def set_document(self, path):
        self.pdf_viewer.set_file(Path(path))
