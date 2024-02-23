from PySide6.QtWidgets import QTextEdit, QSizePolicy
from PySide6.QtGui import Qt


class ResizableTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.on_text_change)

    def on_text_change(self):
        self.setMaximumHeight(self.sizeHint().height())

    def sizeHint(self):
        size = self.document().size().toSize()
        self.document().setTextWidth(self.viewport().width())
        margins = self.contentsMargins()
        height = self.document().size().height() + margins.top() \
                                                 + margins.bottom()
        size.setHeight(height)
        return size

    def resizeEvent(self, event):
        self.on_text_change()
        super().resizeEvent(event)
