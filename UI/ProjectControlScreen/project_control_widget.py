from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
    QLabel
from PySide6.QtCore import Signal
from UI.ProjectControlScreen.project_statistics_widget import ProjectStatisticsWidget


class ProjectControlWidget(QWidget):
    Start_Preprocessing_Signal = Signal()
    Open_Main_App_Signal = Signal()
    Export_Signal = Signal()
    Refresh_Statistics = Signal()

    def __init__(self):
        super(ProjectControlWidget, self).__init__()
        self.statistics_widget = ProjectStatisticsWidget()       # todo: make statistics widget
        self.statistics_widget.Reload_Statistics_Signal.connect(
            lambda: self.Refresh_Statistics.emit()
        )

        self.start_preprocessing_button = QPushButton(text='start preprocessing')
        self.start_preprocessing_button.clicked.connect(
            lambda: self.Start_Preprocessing_Signal.emit()
        )

        self.open_main_app_button = QPushButton(text='open descriptor app')
        self.open_main_app_button.clicked.connect(
            lambda: self.Open_Main_App_Signal.emit()
        )

        self.export_button = QPushButton(text='export')
        self.export_button.clicked.connect(
            lambda: self.Export_Signal.emit()
        )

        top_level_layout = QVBoxLayout()
        top_level_layout.addWidget(self.statistics_widget)
        top_level_layout.addWidget(self.start_preprocessing_button)
        top_level_layout.addWidget(self.open_main_app_button)
        top_level_layout.addWidget(self.export_button)
        self.setLayout(top_level_layout)
        pass
    pass
