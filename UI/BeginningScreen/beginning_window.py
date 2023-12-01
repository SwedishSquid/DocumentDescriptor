from UI.main_window import MainWindow
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from UI.BeginningScreen.select_folder_location_widget\
    import SelectFolderLocationWidget


class BeginningWindow(MainWindow):
    def __init__(self):
        super().__init__()
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

        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        widget.setLayout(layout)
        return widget
