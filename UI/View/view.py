from UI.constant_paths import path_to_pictures
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from UI.View.state_view_widget import StateViewWidget


class View:
    def __init__(self):
        self.q_app = QApplication()
        self.q_app.setWindowIcon(QIcon(str(path_to_pictures.joinpath('file'))))

        self.window = QMainWindow()
        self.window.setWindowTitle("Document Descriptor")
        self.window.setMinimumSize(800, 600)

        widget = StateViewWidget()
        self.window.setCentralWidget(widget)
        pass

    def run(self):
        self.window.show()
        return self.q_app.exec()
