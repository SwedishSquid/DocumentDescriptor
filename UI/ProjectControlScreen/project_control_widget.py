from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
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
            self.Refresh_Statistics.emit
        )
        m = 'start preprocessing'
        m_rus = 'Начать предобработку'
        self.start_preprocessing_button = self._make_button(text=m_rus)
        self.start_preprocessing_button.clicked.connect(
            self.Start_Preprocessing_Signal.emit
        )
        m = 'open descriptor app'
        m_rus = 'Перейти к описанию \n предобработанных документов\n (open descriptor)'
        self.open_main_app_button = self._make_to_descriptor_button(text=m_rus)
        self.open_main_app_button.clicked.connect(
            self.Open_Main_App_Signal.emit
        )
        m = 'export'
        m_rus = 'Экспорт обработанных ранее документов'
        self.export_button = self._make_button(text=m_rus)
        self.export_button.clicked.connect(self.Export_Signal.emit)

        top_level_layout = QVBoxLayout()
        top_level_layout.addStretch()
        top_level_layout.addWidget(self.statistics_widget, 7)

        buttons_v_layout = QVBoxLayout()
        buttons_v_layout.setSpacing(30)
        buttons_v_layout.addWidget(self.start_preprocessing_button)
        buttons_v_layout.addWidget(self.export_button)

        buttons_h_layout = QHBoxLayout()
        buttons_h_layout.addLayout(buttons_v_layout)
        buttons_h_layout.addWidget(self.open_main_app_button)

        top_level_layout.addLayout(buttons_h_layout, 2)
        top_level_layout.addStretch(1)
        self.setLayout(top_level_layout)
        pass

    def set_enabled_for_all_action_buttons(self, enabled: bool):
        self.open_main_app_button.setEnabled(enabled)
        self.start_preprocessing_button.setEnabled(enabled)
        self.export_button.setEnabled(enabled)
        pass

    def _make_button(self, text):
        button = QPushButton(text=text)
        font = QFont('Arial', 12)
        button.setFont(font)
        button.setFixedSize(350, 50)
        return button

    def _make_to_descriptor_button(self, text):
        b = QPushButton(text=text)
        b.setFont(QFont('Arial', 12))
        b.setFixedSize(350, 100)

        b.setStyleSheet("""
                QPushButton {
                    background-color: #009292;
                    border-radius: 40px;
                }
                QPushButton:hover {
                    background-color: #008282;
                }
                QPushButton:pressed {
                    background-color: #008160;
                }
            """)
        return b
    pass
