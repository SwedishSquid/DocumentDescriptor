from PySide6.QtWidgets import QWidget, QProgressBar, QLabel, QPushButton, QVBoxLayout

from UI.MainScreen.control_buttons import ControlButtons


class PreprocessingStatWidget(QWidget):
    def __init__(self, view, parent):
        super().__init__()
        self.parent = parent
        prep_progress = QLabel("doing word ...")
        cancel_button = ControlButtons.create_blank_reject_button("Отменить")
        cancel_button.setFixedSize(100, 50)
        cancel_button.clicked.connect(parent.cancel_preprocessing)
        layout = QVBoxLayout()
        layout.addWidget(prep_progress)
        layout.addWidget(cancel_button)
        self.setLayout(layout)
