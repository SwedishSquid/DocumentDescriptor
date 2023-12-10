from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit,\
    QSizePolicy, QLayout
from PySide6.QtGui import QFont, QPalette, QColorConstants


class Field(QWidget):
    def __init__(self, caption: str):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(self._create_label(caption))
        layout.addWidget(QLineEdit())
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setMinimumWidth(500)

        palette = QPalette()
        palette.setColor(self.backgroundRole(), QColorConstants.Gray)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def _create_label(self, caption: str):
        label = QLabel(caption)
        label.setMargin(10)
        label.setFont(QFont('Arial', 14))
        return label
