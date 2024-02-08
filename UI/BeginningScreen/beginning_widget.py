from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal, Slot
from UI.BeginningScreen.select_folder_location_widget \
    import SelectFolderLocationWidget
from UI.window_menu_bar import MenuBar
from pathlib import Path


class BeginningWidget(QWidget):
    Proceed_Button_Signal = Signal(Path)   #

    def __init__(self):
        super().__init__()


        self._input_path: Path = None

        self._continue_button = self._create_continue_button()
        self.hide_continue_button()

        self.selectFolderLocationWidget = SelectFolderLocationWidget(
            "Путь до исходных файлов", "Введите путь")
        self.selectFolderLocationWidget.Some_Input_Signal.connect(
            self._on_some_input)

        layout = QVBoxLayout()
        layout.addWidget(self.selectFolderLocationWidget)
        layout.addWidget(self._continue_button,
                         alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

    def _create_continue_button(self):
        button = QPushButton("Продолжить")
        button.setFixedWidth(200)
        button.clicked.connect(self._emit_proceed_button_signal)

        size_policy = button.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        button.setSizePolicy(size_policy)
        return button

    def _emit_proceed_button_signal(self):
        if self._input_path is not None:
            self.Proceed_Button_Signal.emit(self._input_path)
        pass

    @Slot()
    def _on_some_input(self, text: str):
        # todo: log input text and path result
        # print(text)
        path = Path(text)
        if path.is_dir() and path.is_absolute():
            self.show_continue_button()
            self._input_path = path
        else:
            self.hide_continue_button()
            self._input_path = None
        pass

    def show_continue_button(self):
        self._continue_button.show()

    def hide_continue_button(self):
        self._continue_button.hide()
