from PySide6.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem
from UI.MainScreen.field_list_item import Field
from PySide6.QtCore import Qt
from PySide6.QtGui import QColorConstants


class FieldList(QListWidget):
    _max_fields_font_size = 30
    def __init__(self, font_size: int):
        super().__init__()
        self.is_changed = False
        self.font_size = font_size

        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(5)
        self.setSpacing(1)

    def add_field(self, caption: str, content: str, name: str):
        item = QListWidgetItem()
        widget = Field(caption, content, name, self.font_size, item)
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
        for field in self._get_all_fields():
            yield field.name, field.get_content()

    def _get_all_fields(self):
        for i in range(self.count()):
            item = self.item(i)
            field: Field = self.itemWidget(item)
            yield field

    def change_fields_font_size(self, new_size: int):
        if new_size <= 0 or new_size > self._max_fields_font_size \
                 or new_size == self.font_size:
            return
        self.font_size = new_size
        for field in self._get_all_fields():
            field.change_font_size(self.font_size)

    def increase_fields_font_size(self):
        self.change_fields_font_size(self.font_size + 1)

    def decrease_fields_font_size(self):
        self.change_fields_font_size(self.font_size - 1)

    def clear(self):
        self.is_changed = False
        super().clear()

    def _on_field_change(self):
        self.is_changed = True

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
        contents_margins_size = self.contentsMargins().left() \
                          + self.contentsMargins().right()
        item_width = self.viewport().width() - contents_margins_size - self.spacing()
        if self.verticalScrollBar().isVisible():
            item_width -= self.verticalScrollBar().width()
        return item_width
