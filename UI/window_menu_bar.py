from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.addMenu(self._create_file_menu())
        self.help_action = QAction("Помощь")
        self.addAction(self.help_action)

    def _create_file_menu(self):
        file_menu = QMenu("Файл")
        self.open_file_action = QAction("Открыть файл")
        self.open_folder_action = QAction("Открыть папку")
        self.open_recent_action = QAction("Открыть недавние...")
        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.open_folder_action)
        file_menu.addAction(self.open_recent_action)
        return file_menu
