from PySide6.QtWidgets import QDialog, QVBoxLayout
from UI.ProjectControlScreen.preprocess_dialog.preprocess_progress_widget import PreprocessProgressWidget
import time


class PreprocessDialog(QDialog):
    def __init__(self):
        super(PreprocessDialog, self).__init__()
        self.widget = PreprocessProgressWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.widget)

        self.setLayout(layout)

    def set_message(self, text: str):
        self.widget.set_message(text)
        pass

    def add_output_text(self, text: str):
        """WARNING: this is dangerous thing - without inner time.sleep(0.01) fails app with memory-leak like message
        I want to think that it is a temporary solution"""
        # todo: investigate the problem - this widget is crashing the app
        # seems that QTextEdit is not thread-safe https://stackoverflow.com/questions/53285181/pyqt5-program-crashes-while-updating-qtextedit-via-logging
        self.widget.add_output_text(text)
        # time.sleep(0.01)
        pass
    pass
