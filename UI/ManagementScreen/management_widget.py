from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton

from UI.MainScreen.control_buttons import ControlButtons
from UI.ManagementScreen.initialized_case_widget import InitializedCaseWidget
from UI.ManagementScreen.not_initialized_case_widget import NotInitializedCaseWidget


class ManagementWidget(QWidget):
    def __init__(self, view):
        super().__init__()
        self.view = view
        layout = QVBoxLayout()
        initialized = True
        self.initialized_case_widget = InitializedCaseWidget(view)
        self.not_initialized_case_widget = NotInitializedCaseWidget(view)
        if initialized:
            layout.addWidget(self.initialized_case_widget)
        else:
            layout.addWidget(self.not_initialized_case_widget)
        self.setLayout(layout)
