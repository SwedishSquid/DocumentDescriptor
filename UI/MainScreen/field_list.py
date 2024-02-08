from PySide6.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem
from UI.MainScreen.field_list_item import Field
from PySide6.QtCore import Qt
from PySide6.QtGui import QColorConstants


class FieldList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(5)
        self.setSpacing(3)

    def add_field(self, caption: str, content: str, name: str):
        item = QListWidgetItem()
        widget = Field(caption, content, name, item)

        self.addItem(item)
        self.setItemWidget(item, widget)
        item.setSizeHint(widget.sizeHint())
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        item.setBackground(QColorConstants.Gray)

    def get_all_fields(self):
        for i in range(self.count()):
            item = self.item(i)
            field = self.itemWidget(item)
            yield field.name, field.get_content()
