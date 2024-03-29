from UI.constant_paths import path_to_pictures
from PySide6.QtGui import QPalette, QColorConstants, QPixmap, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QSizePolicy, QHBoxLayout, QPushButton, QFileDialog
from PySide6.QtCore import Signal


class SelectFolderLocationWidget(QWidget):
    Some_Input_Signal = Signal(str)

    def __init__(self, caption: str, input_field_info: str):
        super().__init__()
        sub_widget = QWidget()
        sub_widget.setLayout(QHBoxLayout())

        self.input_field = self._create_input_field(input_field_info)

        self.input_field.textChanged.connect(self._emit_someinput_signal)

        sub_widget.layout().addWidget(self.input_field)
        sub_widget.layout().addWidget(self._create_enter_file_manager_button())
        sub_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        layout = QVBoxLayout()
        layout.addWidget(self._create_header_label(caption))
        layout.addWidget(sub_widget)
        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setMinimumWidth(500)

        palette = QPalette()
        palette.setColor(self.backgroundRole(), QColorConstants.Gray)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        pass

    def get_input_text(self):
        return self.input_field.text()

    def clear_input_text(self):
        self.input_field.setText('')
        pass

    def _emit_someinput_signal(self):
        self.Some_Input_Signal.emit(self.input_field.text())
        pass

    def _create_header_label(self, caption: str):
        label = QLabel(caption)
        label.setMargin(10)
        label.setFont(QFont('Arial', 14))
        return label

    def _create_input_field(self, info: str):
        input_field = QLineEdit()
        input_field.setFont(QFont('Arial', 12))
        input_field.setPlaceholderText(info)
        return input_field

    def _create_enter_file_manager_button(self):
        button = QPushButton()
        button.setIcon(QPixmap(str(path_to_pictures.joinpath('folder'))))
        button.clicked.connect(self._get_directory)
        return button

    def _get_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            caption="Выбрать папку",
            options=QFileDialog.Option.ShowDirsOnly
        )

        if dir_path:
            self.input_field.setText(dir_path)
