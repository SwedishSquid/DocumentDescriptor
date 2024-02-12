from PySide6.QtCore import Qt, QTime, QTimer, QCoreApplication, QEventLoop, QThread
from PySide6.QtWidgets import QWidget, QProgressBar, QLabel, QPushButton, QVBoxLayout, QDialog, QDialogButtonBox, \
    QSizePolicy
import time


class PreprocessingDialog(QDialog):
    def __init__(self, view, parent):
        super().__init__(parent)
        self.stop_pressed = False
        self.view = view
        self.parent = parent
        self.setWindowTitle("Предобработка")
        self.setMinimumSize(400, 100)
        self.setModal(True)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)

        button_box = QDialogButtonBox(self)
        self.stop_button = QPushButton("Стоп")
        self.proceed_button = QPushButton("Продолжить")
        self.proceed_button.setDisabled(True)
        self.stop_button.setEnabled(True)
        button_box.addButton(self.stop_button, QDialogButtonBox.ButtonRole.RejectRole)
        button_box.addButton(self.proceed_button, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.rejected.connect(self.process_stop)
        button_box.accepted.connect(self.parent.process_preprocess_finish)

        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)
        layout.addWidget(button_box)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def begin_preprocessing(self):
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(1)
        for done, total in self.view.app.glue.get_preprocessor_generator():
            if total < 1 or self.stop_pressed:
                self.stop_preprocessing()
                break
            self.progress_bar.setValue(done / total)
        self.progress_bar.setValue(1)
        self.proceed_button.setEnabled(True)
        self.stop_button.setDisabled(True)

    def process_stop(self):
        self.stop_pressed = True
        self.stop_button.setDisabled(True)

    def stop_preprocessing(self):
        self.stop_pressed = False
