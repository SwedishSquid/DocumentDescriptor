from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QMainWindow
from UI.MainScreen.control_buttons import ControlButtons
# from UI.MainScreen.pdf_viewer import PDFViewer
from UI.MainScreen.reject_qdialog import Reject
from UI.MainScreen.full_book_list_qdialog import FullBookList
from UI.MainScreen.field_list import FieldList
from UI.MainScreen.browser_pdf_viewer import BrowserPdfViewer
from pathlib import Path


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_viewer = BrowserPdfViewer()
        self.pdf_viewer.set_file(Path())
        self.field_list = FieldList()

        layout = QHBoxLayout()
        self.control_buttons = ControlButtons()  # part of public interface
        layout.addWidget(self._create_left_widget(self.control_buttons))
        layout.addWidget(self.pdf_viewer)
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

    def _create_left_widget(self, control_buttons: ControlButtons):
        layout1 = QVBoxLayout()
        layout1.addStretch()
        layout1.addWidget(self.field_list, 4)
        layout1.addWidget(control_buttons, 1)
        widget1 = QWidget()
        widget1.setLayout(layout1)
        return widget1

    def set_document(self, path):
        self.pdf_viewer.set_file(Path(path))
