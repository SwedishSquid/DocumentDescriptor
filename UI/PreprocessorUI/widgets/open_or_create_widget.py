from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal


class OpenOrCreateWidget(QWidget):
    """the very first widget user will see - suggests to choose from 3 options:
    - create a new project
    - open an existing project
    - open recently opened project (coming soon)"""
    Create_New_Project_Signal = Signal()
    Open_Existing_Project_Signal = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_new_button = QPushButton(text='create new')
        self.create_new_button.clicked.connect(
            lambda : self.Create_New_Project_Signal.emit())
        self.open_existing_button = QPushButton(text='open existing')
        self.open_existing_button.clicked.connect(
            lambda: self.Open_Existing_Project_Signal.emit())
        self.recent_projects_widget = QLabel(text='open recent; (coming soon)')

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.create_new_button)
        horizontal_layout.addWidget(self.open_existing_button)

        vertical_layout = QVBoxLayout()
        self.setLayout(vertical_layout)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.recent_projects_widget)
        pass
    pass
