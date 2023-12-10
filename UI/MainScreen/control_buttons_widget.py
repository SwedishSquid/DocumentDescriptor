from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton


class ControlButtons(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.addWidget(QPushButton("Полный список"))
        layout.addWidget(QPushButton("Отмена"))
        layout.addWidget(QPushButton("Продолжить"))

        self.setLayout(layout)
