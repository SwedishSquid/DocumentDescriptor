from PySide6.QtGui import QAction
from PySide6.QtWidgets import QSizePolicy, QMainWindow, QMenuBar, QMenu
from file_menu_widget import FileMenuWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setSizePolicy(size_policy)
        self.setWindowTitle("Document descriptor")
        self.setCentralWidget(FileMenuWidget())
        self.setMenuBar(QMenuBar())
        self.file_menu = QMenu("Файл")
        self.help_action = QAction("Помощь")
        self.open_file_action = QAction("Открыть файл")
        self.open_folder_action = QAction("Открыть папку")
        self.open_recent_action = QAction("Открыть недавние...")
        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addAction(self.help_action)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.open_folder_action)
        self.file_menu.addAction(self.open_recent_action)
