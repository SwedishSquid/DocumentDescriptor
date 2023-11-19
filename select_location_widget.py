import os
from PySide6.QtGui import QPalette, QColorConstants, QPixmap, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QHBoxLayout, QPushButton


class SelectLocationWidget(QWidget):
    def __init__(self, do_selection):
        super().__init__()
        self.select_file_sub_widget = QWidget()
        self.select_file_sub_widget.setLayout(QHBoxLayout())
        self.setLayout(QVBoxLayout())
        self.header_label = QLabel('Путь до исходных файлов' if do_selection else "Где сохранить результат")
        self.header_label.setMargin(10)
        self.header_label.setFont(QFont('Arial', 14))
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(f"*путь до {'файла или ' if do_selection else ''}папки*")
        self.enter_file_manager_context_button = QPushButton()  # к этой кнопке надо прикрутить тот самый функционал
        self.enter_file_manager_context_button.setIcon(
            QPixmap(os.path.join('resources', 'folder')))
        self.layout().addWidget(self.header_label)
        self.layout().addWidget(self.select_file_sub_widget)
        self.select_file_sub_widget.layout().addWidget(self.input_field)
        self.select_file_sub_widget.layout().addWidget(self.enter_file_manager_context_button)
        self.select_file_sub_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColorConstants.Gray)
        self.setAutoFillBackground(True)
        self.setPalette(self.palette)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
        self.setMinimumWidth(500)
