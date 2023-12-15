from UI.MainScreen.list_widget_item_field import Field
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout,\
    QWidget, QVBoxLayout, QAbstractItemView, QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtGui import QColorConstants
from UI.MainScreen.control_buttons_widget import ControlButtons
from UI.MainScreen.pdf_viewer import PDFViewer
from UI.window_menu_bar import MenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document descriptor")
        self.setMenuBar(MenuBar())

        layout = QHBoxLayout()
        layout.addWidget(self._create_left_widget())
        layout.addWidget(PDFViewer())
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def _create_left_widget(self):
        layout1 = QVBoxLayout()
        layout1.addStretch()
        layout1.addWidget(self._create_list_widgets(), 4)
        layout1.addWidget(ControlButtons(), 1)
        widget1 = QWidget()
        widget1.setLayout(layout1)
        return widget1

    def _create_list_widgets(self):
        list_widget = QListWidget()
        for i in range(15):
            item = QListWidgetItem()
            widget = Field("Автор" + str(i))

            item.setSizeHint(widget.size())
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            item.setBackground(QColorConstants.Gray)
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)

        list_widget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        list_widget.setSpacing(3)
        return list_widget
