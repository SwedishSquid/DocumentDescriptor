from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QMainWindow
from UI.MainScreen.control_buttons import ControlButtons
from UI.MainScreen.pdf_viewer import PDFViewer
from UI.window_menu_bar import MenuBar
from UI.MainScreen.list_fields import ListFields


class MainWindow(QMainWindow):
    def __init__(self, view):
        super().__init__()

        self.setWindowTitle("Document descriptor")
        self.setMenuBar(MenuBar())
        self.pdf_viewer = PDFViewer()
        self.list_fields = ListFields()

        layout = QHBoxLayout()
        layout.addWidget(self._create_left_widget(view))
        layout.addWidget(self.pdf_viewer)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def _create_left_widget(self, view):
        layout1 = QVBoxLayout()
        layout1.addStretch()
        layout1.addWidget(self.list_fields, 4)
        layout1.addWidget(ControlButtons(view), 1)
        widget1 = QWidget()
        widget1.setLayout(layout1)
        return widget1
