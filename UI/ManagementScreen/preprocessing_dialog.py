from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QProgressBar, QLabel, QPushButton, QVBoxLayout, QDialog, QDialogButtonBox

from UI.MainScreen.control_buttons import ControlButtons


class PreprocessingDialog(QDialog):
    def __init__(self, view, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Предобработка")
        self.setMinimumSize(400, 300)
        self.setModal(True)
        layout = QVBoxLayout(self)
        msg = QLabel(self)
        msg.setText("doing word ...")
        layout.addWidget(msg)

        button_box = QDialogButtonBox(self)
        stop_button = QPushButton("Стоп")
        proceed_button = QPushButton("Продолжить")
        proceed_button.setDisabled(True)
        button_box.addButton(stop_button, QDialogButtonBox.ButtonRole.RejectRole)
        button_box.addButton(proceed_button, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.rejected.connect(self.stop_preprocessing)
        button_box.accepted.connect(self.stop_preprocessing)
        layout.addWidget(button_box)

    def begin_preprocessing(self):
        pass

    def stop_preprocessing(self):
        self.close()
        pass
