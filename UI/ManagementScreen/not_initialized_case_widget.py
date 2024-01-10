from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from UI.MainScreen.control_buttons import ControlButtons


class NotInitializedCaseWidget(QWidget):

    def __init__(self, view):
        super().__init__()
        self.view = view
        layout = QVBoxLayout()
        msg = QLabel(
            """Похоже, вы впервые открыли эту библиотеку.\nПеред началом работы необходимо произвести подготовку.""")
        msg.setFont(QFont('Arial', 20))
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_widget = QWidget()
        buttons_widget.setLayout(QHBoxLayout())
        buttons_widget.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        continue_button = ControlButtons.create_blank_continue_button("Продолжить")
        continue_button.setFixedSize(QSize(200, 100))
        reject_button = ControlButtons.create_blank_reject_button("Отмена")
        reject_button.setFixedSize(QSize(200, 100))
        buttons_widget.layout().addWidget(continue_button)
        buttons_widget.layout().addWidget(reject_button)

        continue_button.clicked.connect(view.init_project)
        reject_button.clicked.connect(view.switch_to_beginning_widget)

        layout.addWidget(msg)
        layout.addWidget(buttons_widget)

        self.setLayout(layout)
