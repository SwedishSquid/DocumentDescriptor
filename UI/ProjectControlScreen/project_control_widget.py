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
        self.statistics_widget = ProjectStatisticsWidget()
        self.statistics_widget.Reload_Statistics_Signal.connect(
            lambda: self.Refresh_Statistics.emit()
        )
        m = 'start preprocessing'
        m_rus = 'Начать предобработку'
        self.start_preprocessing_button = QPushButton(text=m_rus)
        self.start_preprocessing_button.clicked.connect(
            lambda: self.Start_Preprocessing_Signal.emit()
        )
        m = 'open descriptor app'
        m_rus = 'Перейти к описанию предобработанных документов'
        self.open_main_app_button = QPushButton(text=m_rus)
        self.open_main_app_button.clicked.connect(
            lambda: self.Open_Main_App_Signal.emit()
        )
        m = 'export'
        m_rus = 'Экспорт обработанных ранее документов'
        self.export_button = QPushButton(text=m_rus)
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

    def set_enabled_for_all_action_buttons(self, enabled: bool):
        self.open_main_app_button.setEnabled(enabled)
        self.start_preprocessing_button.setEnabled(enabled)
        self.export_button.setEnabled(enabled)
        pass
    pass
