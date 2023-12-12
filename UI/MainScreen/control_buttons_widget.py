from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton


class ControlButtons(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.addWidget(self._create_full_list_button_())
        layout.addWidget(QPushButton("Отмена"))
        layout.addWidget(QPushButton("Продолжить"))

        self.setLayout(layout)

    def _create_full_list_button_(self):
        button = QPushButton("Полный список")
        button.setFixedSize(150, 100)
        button.setStyleSheet("""
                QPushButton {
                    background-color: yellow;
                    border-radius: 40px;
                }
                QPushButton:hover {
                    background-color: lightblue;
                }
                QPushButton:pressed {
                    background-color: blue;
                }
            """)
        return button
