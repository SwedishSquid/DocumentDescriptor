from PySide6.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout,\
    QWidget, QVBoxLayout, QAbstractItemView
from UI.MainScreen.list_item_field import Field
from PySide6.QtCore import Qt
from PySide6.QtGui import QColorConstants


class ListFields(QListWidget):
    def __init__(self):
        super().__init__()
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setSpacing(3)

    def add_field(self, caption: str, content: str, name: str):
        item = QListWidgetItem()
        widget = Field(caption, content, name)

        item.setSizeHint(widget.size())
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        item.setBackground(QColorConstants.Gray)
        self.addItem(item)
        self.setItemWidget(item, widget)

    def get_all_fields(self):
        for i in range(self.count()):
            item = self.item(i)
            field = self.itemWidget(item)
            yield field.name, field.get_content()
