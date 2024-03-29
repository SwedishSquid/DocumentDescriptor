from UI.constant_paths import path_to_pictures

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import QSize, QKeyCombination, Qt


class ControlButtons(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.full_list_button = self._create_full_list_button_()
        self.reject_button = self._create_reject_button()
        self.continue_button = self._create_continue_button()

        layout.addWidget(self.full_list_button)
        layout.addWidget(self.reject_button)
        layout.addWidget(self.continue_button)

        self.setLayout(layout)

    def _create_full_list_button_(self):
        button = QPushButton("Полный\n"
                             "список")

        button.setShortcut(QKeyCombination(Qt.Modifier.CTRL, Qt.Key.Key_L))
        button.setToolTip("Показать список всех документов <b>Ctrl+L</b>")

        font = QFont('Arial', 16)
        font.setBold(True)
        button.setFont(font)

        button.setFixedSize(150, 100)

        button.setStyleSheet("""
                QPushButton {
                    background-color: #FFFF40;
                    border-radius: 40px;
                }
                QPushButton:hover {
                    background-color: #D1D140;
                }
                QPushButton:pressed {
                    background-color: #A1A140;
                }
            """)
        return button

    def _create_reject_button(self):
        button = self.create_blank_reject_button()

        button.setShortcut(QKeyCombination(Qt.Modifier.CTRL, Qt.Key.Key_R))
        button.setToolTip("Отменить <b>Ctrl+R</b>")

        button.setIcon(QPixmap(str(path_to_pictures.joinpath('cross'))))
        button.setIconSize(QSize(96, 96))

        button.setFixedSize(120, 100)

        return button

    def _create_continue_button(self):
        button = self.create_blank_continue_button()

        button.setShortcut(QKeyCombination(Qt.Modifier.CTRL, Qt.Key.Key_N))
        button.setToolTip("Перейти к следующему <b>Ctrl+N</b>")

        button.setIcon(QPixmap(str(path_to_pictures.joinpath('right-arrow'))))
        button.setIconSize(QSize(96, 96))

        button.setFixedSize(150, 100)
        return button

    @staticmethod
    def create_blank_continue_button(text="", border_radius=40):
        button = QPushButton(text)
        button.setStyleSheet("""
                        QPushButton {
                            background-color: #91FF3A;
                            border-radius: %spx;
                        }
                        QPushButton:hover {
                            background-color: #7FDB3A;
                        }
                        QPushButton:pressed {
                            background-color: #70C13A;
                        }
                    """ % str(border_radius))
        return button

    @staticmethod
    def create_blank_reject_button(text="", border_radius=40):
        button = QPushButton(text)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet("""
                        QPushButton {
                            background-color: #FF4040;
                            border-radius: %spx;
                        }
                        QPushButton:hover {
                            background-color: #D14040;
                        }
                        QPushButton:pressed {
                            background-color: #A14040;
                        }
                    """ % str(border_radius))
        return button
