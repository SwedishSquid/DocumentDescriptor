from UI.constant_paths import path_to_pictures
from UI.MainScreen.reject_qdialog import Reject
from UI.MainScreen.full_book_list_qdialog import FullBookList
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import QSize


class ControlButtons(QWidget):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.reject_dialog = Reject(self.view)
        self.full_book_list_dialog = FullBookList(self.view)

        layout = QHBoxLayout()
        layout.addWidget(self._create_full_list_button_())
        layout.addWidget(self._create_reject_button())
        layout.addWidget(self._create_continue_button())

        self.setLayout(layout)

    def _create_full_list_button_(self):
        button = QPushButton("Полный\n"
                             "список")
        button.clicked.connect(
            lambda:
            self.view.show_full_book_list(
                self.full_book_list_dialog.book_list))
        button.clicked.connect(self.full_book_list_dialog.run)

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
        button = QPushButton()
        button.clicked.connect(self.reject_dialog.run)

        button.setIcon(QPixmap(str(path_to_pictures.joinpath('cross'))))
        button.setIconSize(QSize(96, 96))

        button.setFixedSize(120, 100)

        button.setFont(QFont('Arial', 14))

        button.setStyleSheet("""
                        QPushButton {
                            background-color: #FF4040;
                            border-radius: 40px;
                        }
                        QPushButton:hover {
                            background-color: #D14040;
                        }
                        QPushButton:pressed {
                            background-color: #A14040;
                        }
                    """)
        return button

    def _create_continue_button(self):
        button = QPushButton()
        button.clicked.connect(self.view.save_book_meta_as_finished)
        button.clicked.connect(self.view.show_next_book)

        button.setIcon(QPixmap(str(path_to_pictures.joinpath('right-arrow'))))
        button.setIconSize(QSize(96, 96))

        button.setFixedSize(150, 100)

        button.setFont(QFont('Arial', 14))

        button.setStyleSheet("""
                        QPushButton {
                            background-color: #91FF3A;
                            border-radius: 40px;
                        }
                        QPushButton:hover {
                            background-color: #7FDB3A;
                        }
                        QPushButton:pressed {
                            background-color: #70C13A;
                        }
                    """)
        return button
