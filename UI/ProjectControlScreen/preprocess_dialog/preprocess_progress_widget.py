from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtGui import QFont


class PreprocessProgressWidget(QWidget):
    def __init__(self):
        super(PreprocessProgressWidget, self).__init__()
        self.message = QLabel('message here')
        self.message.setFont(QFont("Arial", 10))
        self.output_console = QTextEdit()
        self.output_console.setFont(QFont("Arial", 12))
        self.output_console.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(self.output_console)
        self.setLayout(layout)
        pass

    def set_message(self, text: str):
        self.message.setText(text)
        pass

    def add_output_text(self, text: str):
        self.output_console.insertPlainText(text + '\n')
        pass

    pass
