from PySide6.QtWidgets import QDialog, QVBoxLayout
from UI.PreprocessorUI.preprocess_dialog.preprocess_progress_widget import PreprocessProgressWidget


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
        self.widget.add_output_text(text)
        pass
    pass
