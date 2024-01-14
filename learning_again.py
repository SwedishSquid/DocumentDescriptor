from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Slot, Signal
import random
from pathlib import Path


class TestWidget(QWidget):
    pass


class WidgetWithButton(QWidget):
    button_clicked_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.button = QPushButton(parent=self, text='i am button')
        self.button.clicked.connect(self._button_clicked_event)
        pass

    @Slot()
    def _button_clicked_event(self):
        self.button_clicked_signal.emit(str(random.randint(0, 100)))
        print('signal emitted')


class WidgetWithLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel(parent = self, text='initial text')
        pass

    # @Slot()
    def set_text(self, text: str):
        print('signal received')
        self.label.setText(text)
        pass
    pass


def run():
    app = QApplication()

    window = QMainWindow()

    layout = QVBoxLayout(window)

    w1 = TestWidget()
    w1.setLayout(layout)

    button_widget = WidgetWithButton()
    button_widget.setParent(w1)
    layout.addWidget(button_widget)

    label_widget = WidgetWithLabel()
    label_widget.setParent(w1)
    layout.addWidget(label_widget)

    button_widget.button_clicked_signal.connect(label_widget.set_text)

    window.setCentralWidget(w1)

    window.show()

    app.exec()


# run()

