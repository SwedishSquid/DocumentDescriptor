from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Signal


class InformDialog(QDialog):
    _Set_Info_Message = Signal(str)

    def __init__(self):
        super(InformDialog, self).__init__()
        self.widget = QLabel()
        self.widget.setWordWrap(True)
        self._Set_Info_Message.connect(self._set_info_message)
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        self.setMinimumSize(300, 300)
        self.setLayout(layout)
        pass

    def set_info_message_thread_safe(self, message: str):
        self._Set_Info_Message.emit(message)
        pass

    def _set_info_message(self, message: str):
        self.widget.setText(message)
        pass
    pass
