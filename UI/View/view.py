from UI.constant_paths import path_to_pictures
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from UI.View.state_view_widget import StateViewWidget
import logging
import version


class View:
    def __init__(self):
        self.q_app = QApplication()
        self.q_app.setWindowIcon(QIcon(str(path_to_pictures.joinpath('file'))))

        self.window = QMainWindow()
        self.window.setWindowTitle(f"Document Descriptor {version.get_version()}")
        self.window.setMinimumSize(800, 600)

        widget = StateViewWidget(self.window)
        self.window.setCentralWidget(widget)
        pass

    def run(self):
        logging.info(f'app started; current version = {version.get_version()}')
        self.window.show()
        return self.q_app.exec()
