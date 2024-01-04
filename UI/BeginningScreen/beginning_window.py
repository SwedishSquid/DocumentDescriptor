from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QPushButton
from PySide6.QtCore import Qt
from UI.BeginningScreen.select_folder_location_widget\
    import SelectFolderLocationWidget
from UI.window_menu_bar import MenuBar


class BeginningWindow(QMainWindow):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.setWindowTitle("Document descriptor")
        self.setMenuBar(MenuBar())

        self._continue_button = self._create_continue_button()
        self.hide_continue_button()

        self.setCentralWidget(self._create_central_widget())

    def _create_central_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(
            SelectFolderLocationWidget(
                "Путь до исходных файлов", "Введите путь", self.view))

        layout.addWidget(self._continue_button,
                         alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        widget.setLayout(layout)
        return widget

    def _create_continue_button(self):
        button = QPushButton("Продолжить")
        button.setFixedWidth(200)
        button.clicked.connect(self.view.show_main_window)

        return button

    def show_continue_button(self):
        self._continue_button.show()

    def hide_continue_button(self):
        self._continue_button.hide()
