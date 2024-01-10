from PySide6.QtCore import QThread
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QStackedWidget, QVBoxLayout, QSpacerItem

from UI.ManagementScreen.preprocessing_dialog import PreprocessingDialog


class PreprocessingWidget(QWidget):
    def __init__(self, view):
        super().__init__()
        header = QLabel("Предобработка")
        header.setFont(QFont("Arial", 20))
        self.begin_preprocessing_button = QPushButton("Начать предобработку")
        self.begin_preprocessing_button.setFixedSize(200, 100)
        self.begin_preprocessing_button.clicked.connect(self.begin_preprocessing)
        self.dialog = PreprocessingDialog(view, self)
        self.dialog.setParent(self)

        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addSpacerItem(QSpacerItem(20, 20))
        layout.addWidget(self.begin_preprocessing_button)
        self.setLayout(layout)

        if view.app.glue.is_preprocessed():
            self.process_preprocess_finish()

    def begin_preprocessing(self):
        self.dialog.open()
        self.dialog.begin_preprocessing()

    def process_preprocess_finish(self):
        self.begin_preprocessing_button.setText("Готово")
        self.begin_preprocessing_button.setDisabled(True)
        self.dialog.close()
