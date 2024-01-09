from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QStackedWidget, QVBoxLayout, QSpacerItem

from UI.ManagementScreen.preprocessing_dialog import PreprocessingDialog


class PreprocessingWidget(QWidget):
    def __init__(self, view):
        super().__init__()
        self.dialog = PreprocessingDialog(view, self)
        header = QLabel("Предобработка")
        header.setFont(QFont("Arial", 20))
        self.begin_preprocessing_button = QPushButton("Начать предобработку")
        self.begin_preprocessing_button.setFixedSize(200, 100)
        self.begin_preprocessing_button.clicked.connect(self.dialog.show)

        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addSpacerItem(QSpacerItem(20, 20))
        layout.addWidget(self.begin_preprocessing_button)
        self.setLayout(layout)