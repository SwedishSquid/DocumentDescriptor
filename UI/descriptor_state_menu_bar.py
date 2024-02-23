from PySide6.QtWidgets import QMenu, QMenuBar
from PySide6.QtGui import QAction


class DescriptorStateMenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.addMenu(self._create_fields_menu())

    def _create_fields_menu(self):
        fields_menu = QMenu("Поля")
        self.increase_font_size = QAction("Увеличить шрифт")
        self.decrease_font_size = QAction("Уменьшить шрифт")
        fields_menu.addAction(self.increase_font_size)
        fields_menu.addAction(self.decrease_font_size)
        return fields_menu
