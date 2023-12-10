from PySide6.QtGui import QAction
from PySide6.QtWidgets import QSizePolicy, QMainWindow, QMenuBar, QMenu


class AMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWindowTitle("Document descriptor")
        self.setMenuBar(self._create_menu_bar())

    def _create_menu_bar(self):
        menu_bar = QMenuBar()
        menu_bar.addMenu(self._create_file_menu())
        self.help_action = QAction("Помощь")
        menu_bar.addAction(self.help_action)
        return menu_bar

    def _create_file_menu(self):
        file_menu = QMenu("Файл")
        self.open_file_action = QAction("Открыть файл")
        self.open_folder_action = QAction("Открыть папку")
        self.open_recent_action = QAction("Открыть недавние...")
        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.open_folder_action)
        file_menu.addAction(self.open_recent_action)
        return file_menu
