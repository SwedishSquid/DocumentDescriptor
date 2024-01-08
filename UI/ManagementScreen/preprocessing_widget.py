from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QStackedWidget, QVBoxLayout, QSpacerItem

from UI.ManagementScreen import preprocessing_stat_widget
from UI.ManagementScreen.preprocessing_stat_widget import PreprocessingStatWidget


class PreprocessingWidget(QWidget):
    def __init__(self, view):
        super().__init__()
        header = QLabel("Предобработка")
        header.setFont(QFont("Arial", 20))
        self.functional_widget = QStackedWidget()

        self.begin_preprocessing_button = QPushButton("Начать предобработку")
        self.begin_preprocessing_button.setFixedSize(200, 100)
        self.begin_preprocessing_button.clicked.connect(self.begin_preprocessing)
        self.preprocessing_stat_widget = PreprocessingStatWidget(view, self)

        self.functional_widget.addWidget(self.begin_preprocessing_button)
        self.functional_widget.addWidget(self.preprocessing_stat_widget)
        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addSpacerItem(QSpacerItem(20, 20))
        layout.addWidget(self.functional_widget)
        self.setLayout(layout)

    def begin_preprocessing(self):
        self.functional_widget.setCurrentWidget(self.preprocessing_stat_widget)
        pass

    def cancel_preprocessing(self):
        self.functional_widget.setCurrentWidget(self.begin_preprocessing_button)
