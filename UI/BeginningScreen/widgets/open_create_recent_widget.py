from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont
from UI.BeginningScreen.widgets.recent_projects_widget import RecentProjectsWidget
from pathlib import Path


class OpenCreateRecentWidget(QWidget):
    """the very first widget user will see - suggests to choose from 3 options:
    - create a new project
    - open an existing project
    - open recently opened project (coming soon)"""
    Create_New_Project_Signal = Signal()
    Open_Existing_Project_Signal = Signal()
    Open_Recent_Project_Signal = Signal(Path)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        m = 'create new'
        m_rus = 'Создать новый проект'
        self.create_new_button = self._make_button(m_rus)
        self.create_new_button.clicked.connect(
            lambda: self.Create_New_Project_Signal.emit())
        m = 'open existing'
        m_rus = 'Открыть существующий проект'
        self.open_existing_button = self._make_button(m_rus)
        self.open_existing_button.clicked.connect(
            lambda: self.Open_Existing_Project_Signal.emit())
        m = 'open recent; (coming soon)'
        m_rus = 'Недавно открытые проекты (В версии 1.1.0 еще не сделано)'

        self.recent_projects_widget = RecentProjectsWidget()
        self.recent_projects_widget.Project_Selected_Signal.connect(
            self.Open_Recent_Project_Signal.emit
        )

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.create_new_button,
                                    alignment=Qt.AlignmentFlag.AlignVCenter)
        horizontal_layout.addWidget(self.open_existing_button,
                                    alignment=Qt.AlignmentFlag.AlignVCenter)

        vertical_layout = QVBoxLayout()
        self.setLayout(vertical_layout)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.recent_projects_widget)
        pass

    def _make_button(self, text):
        button = QPushButton(text=text)
        font = QFont('Arial', 12)
        button.setFont(font)
        button.setFixedSize(270, 50)
        return button

    def set_recent_projects(self, project_paths: list):
        self.recent_projects_widget.set_project_paths(project_paths)
        pass
    pass
