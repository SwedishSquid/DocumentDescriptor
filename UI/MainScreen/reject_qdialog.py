from PySide6.QtWidgets import QDialog, QWidget, QPushButton, QLabel,\
    QTextEdit, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class Reject(QDialog):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.setWindowTitle("Окно отклонения")
        self.resize(500, 250)

        layout = QVBoxLayout()
        self._text_edit = self._create_line_edit()

        layout.addWidget(self._create_central_widget())
        layout.addWidget(self._create_confirm_button())

        self.setLayout(layout)

    def run(self):
        self.exec()

    def _create_central_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self._create_label("Причина отклонения документа"), 1)
        layout.addWidget(self._text_edit, 5)
        widget.setLayout(layout)
        widget.setMaximumHeight(100)
        return widget

    def _create_label(self, caption: str):
        label = QLabel(caption)
        label.setMargin(10)
        label.setFont(QFont('Arial', 14))
        return label

    def _create_line_edit(self):
        text_edit = QTextEdit()
        text_edit.setMinimumHeight(50)
        text_edit.setFont(QFont('Arial', 14))

        return text_edit

    def _create_confirm_button(self):
        button = QPushButton("Подтвердить")
        button.setMaximumWidth(100)
        button.clicked.connect(lambda: self.done(2))
        button.clicked.connect(self.view.save_book_meta_as_rejected)
        button.clicked.connect(self.view.show_next_book)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setMaximumHeight(100)
        return widget
