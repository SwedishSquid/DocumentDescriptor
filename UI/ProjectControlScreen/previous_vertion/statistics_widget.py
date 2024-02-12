from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem


class StatisticsWidget(QWidget):
    def __init__(self, view):
        super().__init__()
        layout = QVBoxLayout()
        header = QLabel("Статистика")
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header.setFont(QFont('Arial', 20))

        property1 = self.get_property_label("Свойство1 : ...")
        property2 = self.get_property_label("Свойство2 : ...")

        layout.addWidget(header)
        layout.addSpacerItem(QSpacerItem(20, 20))
        layout.addWidget(property1)
        layout.addWidget(property2)
        self.setLayout(layout)

    @staticmethod
    def get_property_label(text=""):
        label = QLabel(text)
        label.setFont(QFont('Arial', 12))
        return label
