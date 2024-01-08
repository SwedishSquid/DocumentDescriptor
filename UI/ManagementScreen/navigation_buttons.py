from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QVBoxLayout

from UI.MainScreen.control_buttons import ControlButtons


class NavigationButtons(QWidget):
    def __init__(self, view):
        super().__init__()
        self.view = view
        begin_editing_button = ControlButtons.create_blank_continue_button("Начать работу")
        begin_editing_button.clicked.connect(self.view.switch_to_main_widget)
        begin_editing_button.setFixedSize(200, 50)

        back_button = ControlButtons.create_blank_reject_button("Назад")
        back_button.clicked.connect(self.view.switch_to_beginning_widget)
        back_button.setFixedSize(200, 50)

        layout = QVBoxLayout()
        layout.addWidget(begin_editing_button)
        layout.addWidget(back_button)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
