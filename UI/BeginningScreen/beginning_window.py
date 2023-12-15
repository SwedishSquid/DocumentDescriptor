from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QPushButton
from PySide6.QtCore import Qt
from UI.BeginningScreen.select_folder_location_widget\
    import SelectFolderLocationWidget
from UI.window_menu_bar import MenuBar


class BeginningWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document descriptor")
        self.setMenuBar(MenuBar())

        self.setCentralWidget(self._create_select_folders_widget())

    def _create_select_folders_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(
            SelectFolderLocationWidget(
                "Путь до исходных файлов", "Введите путь"))
        layout.addWidget(
            SelectFolderLocationWidget(
                "Где сохранить результат", "Введите путь"))

        layout.addWidget(self._create_continue_button())

        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        widget.setLayout(layout)
        return widget

    def _create_continue_button(self):
        widget = QWidget()
        layout = QVBoxLayout()
        button = QPushButton("Продолжить")
        button.setMinimumWidth(200)
        layout.addWidget(button)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        widget.setLayout(layout)

        return widget

