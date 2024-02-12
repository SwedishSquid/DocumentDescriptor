from PySide6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from UI.ProjectControlScreen.previous_vertion.navigation_buttons import NavigationButtons
from UI.ProjectControlScreen.previous_vertion.preprocessing_widget import PreprocessingWidget
from UI.ProjectControlScreen.previous_vertion.statistics_widget import StatisticsWidget


class InitializedCaseWidget(QWidget):

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.statistics_widget = None
        self.preprocessing_widget = None

    def reset(self):
        view = self.view
        self.statistics_widget = StatisticsWidget(view)
        self.preprocessing_widget = PreprocessingWidget(view)
        layout = QVBoxLayout()
        layout.addWidget(self.statistics_widget)
        layout.addSpacerItem(QSpacerItem(20, 20))
        layout.addWidget(self.preprocessing_widget)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))
        layout.addWidget(NavigationButtons(view))
        self.setLayout(layout)
