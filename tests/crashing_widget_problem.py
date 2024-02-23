from UI.ProjectControlScreen.preprocess_dialog.preprocess_dialog import PreprocessDialog
from threading import Thread
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
import time


class MyWidget(QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.button = QPushButton(text='start test')
        self.button.clicked.connect(self.start_test)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.dialog = PreprocessDialog()
        pass

    def start_test(self):
        def funci():
            time.sleep(0.1)
            payload = 'jklsdhfkjshdkjf' * 10
            for i in range(3200):
                message = f'{i} : {payload}'
                self.dialog.add_output_text(message)
                print(i)
                time.sleep(0.01)
            pass

        thread = Thread(target=funci)
        thread.start()
        self.dialog.exec()
        thread.join()


def dialog_load():
    app = QApplication()
    window = QMainWindow()
    window.setWindowTitle('test dialog')
    window.setMinimumSize(800, 600)

    """currently the problem is 'solved' inside the dialog thing;
     might be able to replicate via calling insertPlainText of QTextEdit settled in a dialog box; calling from another thread with almost no time inbetween calls"""
    w = MyWidget()
    window.setCentralWidget(w)

    window.show()
    app.exec()





dialog_load()
