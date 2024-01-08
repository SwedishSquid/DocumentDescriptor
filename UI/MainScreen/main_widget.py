from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QMainWindow
from UI.MainScreen.control_buttons import ControlButtons
# from UI.MainScreen.pdf_viewer import PDFViewer
from UI.window_menu_bar import MenuBar
from UI.MainScreen.field_list import FieldList
from UI.MainScreen.browser_pdf_viewer import BrowserPdfViewer
from pathlib import Path


class MainWidget(QWidget):
    def __init__(self, view):
        super().__init__()

        self.setWindowTitle("Document descriptor")
        self.pdf_viewer = BrowserPdfViewer()
        self.pdf_viewer.set_file(Path("E:/dev/DocumentDescriptor/DocumentDescriptor/dir_that_git_ignores/2/test.pdf"))
        self.field_list = FieldList()

        layout = QHBoxLayout()
        layout.addWidget(self._create_left_widget(view))
        layout.addWidget(self.pdf_viewer)
        self.setLayout(layout)

    def _create_left_widget(self, view):
        layout1 = QVBoxLayout()
        layout1.addStretch()
        layout1.addWidget(self.field_list, 4)
        layout1.addWidget(ControlButtons(view), 1)
        widget1 = QWidget()
        widget1.setLayout(layout1)
        return widget1

    def set_document(self, path):
        self.pdf_viewer.set_file(Path(path))
