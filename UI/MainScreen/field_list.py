from PySide6.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem
from UI.MainScreen.field_list_item import Field
from PySide6.QtCore import Qt
from PySide6.QtGui import QColorConstants


class FieldList(QListWidget):
    def __init__(self):
        super().__init__()
        self.is_change = False

        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(5)
        self.setSpacing(3)

    def add_field(self, caption: str, content: str, name: str):
        item = QListWidgetItem()
        widget = Field(caption, content, name, item)
        widget.text_edit.textChanged.connect(self._on_field_change)
        widget.enterPressed.connect(self._on_enter_press)
        self.addItem(item)
        self.setItemWidget(item, widget)

        size_hint = widget.sizeHint()
        size_hint.setWidth(self._item_view_width())
        item.setSizeHint(size_hint)

        item.setFlags(Qt.ItemFlag.NoItemFlags)
        item.setBackground(QColorConstants.Gray)

    def get_all_fields(self):
        for i in range(self.count()):
            item = self.item(i)
            field = self.itemWidget(item)
            yield field.name, field.get_content()

    def clear(self):
        self.is_change = False
        super().clear()

    def _on_enter_press(self, item: QListWidgetItem):
        next_idx = self.indexFromItem(item).row() + 1
        if next_idx < self.count():
            next_item = self.item(next_idx)
            self.scrollToItem(next_item,
                              QAbstractItemView.ScrollHint.EnsureVisible)
            next_field: Field = self.itemWidget(next_item)
            next_field.make_active()

    def resizeEvent(self, e):
        self._resize_items()
        super().resizeEvent(e)

    def _resize_items(self):
        item_width = self._item_view_width()
        for i in range(self.count()):
            item = self.item(i)
            size_hint = item.sizeHint()
            size_hint.setWidth(item_width)
            item.setSizeHint(size_hint)

    def _item_view_width(self):
        item_width = self.viewport().width()
        if self.verticalScrollBar().isVisible():
            item_width -= self.verticalScrollBar().width()
        return item_width

    def _on_field_change(self):
        self.is_change = True
