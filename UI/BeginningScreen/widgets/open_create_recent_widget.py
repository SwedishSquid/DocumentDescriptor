from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal


class OpenCreateRecentWidget(QWidget):
    """the very first widget user will see - suggests to choose from 3 options:
    - create a new project
    - open an existing project
    - open recently opened project (coming soon)"""
    Create_New_Project_Signal = Signal()
    Open_Existing_Project_Signal = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        m = 'create new'
        m_rus = 'Создать новый проект'
        self.create_new_button = QPushButton(text=m_rus)
        self.create_new_button.clicked.connect(
            lambda : self.Create_New_Project_Signal.emit())
        m = 'open existing'
        m_rus = 'Открыть существующий проект'
        self.open_existing_button = QPushButton(text=m_rus)
        self.open_existing_button.clicked.connect(
            lambda: self.Open_Existing_Project_Signal.emit())
        m = 'open recent; (coming soon)'
        m_rus = 'Недавно открытые проекты (В версии 1.1.0 еще не сделано)'
        self.recent_projects_widget = QLabel(text=m_rus)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.create_new_button)
        horizontal_layout.addWidget(self.open_existing_button)

        vertical_layout = QVBoxLayout()
        self.setLayout(vertical_layout)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.recent_projects_widget)
        pass
    pass
