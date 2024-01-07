from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PySide6.QtGui import QFont


class NoMoreFilesDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Книги закончились!')
        self.setFixedSize(500, 250)

        layout = QVBoxLayout()

        label = QLabel(text='Документов больше нет. Поздравляем!')
        label.setMargin(10)
        label.setFont(QFont('Arial', 14))
        layout.addWidget(label)

        self.setLayout(layout)
        pass
