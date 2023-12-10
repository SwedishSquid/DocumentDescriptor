from UI.abstract_main_window import AMainWindow
from UI.MainScreen.list_widget_item_field import Field
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout, QWidget, QVBoxLayout
from UI.MainScreen.control_buttons_widget import ControlButtons
from UI.MainScreen.pdf_viewer import PDFViewer


class MainWindow(AMainWindow):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.addWidget(self._create_left_widget())
        layout.addWidget(PDFViewer())
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def _create_left_widget(self):
        layout1 = QVBoxLayout()
        layout1.addWidget(self._create_list_widgets())
        layout1.addWidget(ControlButtons())
        widget1 = QWidget()
        widget1.setLayout(layout1)
        return widget1

    def _create_list_widgets(self):
        _list = QListWidget()
        for i in range(15):
            item = QListWidgetItem()
            widget = Field("Автор" + str(i))
            item.setSizeHint(widget.sizeHint())
            _list.addItem(item)
            _list.setItemWidget(item, widget)
        return _list
