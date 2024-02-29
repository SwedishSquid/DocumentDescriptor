from PySide6.QtWidgets import QWidget,\
    QListWidget, QLabel, QListWidgetItem, \
    QVBoxLayout, QAbstractItemView
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal
from pathlib import Path


class LoadedQListWidgetItem(QListWidgetItem):
    def __init__(self, payload, *args, **kwargs):
        super(LoadedQListWidgetItem, self).__init__(*args, **kwargs)
        self.payload = payload
        pass


class RecentProjectsWidget(QWidget):
    Project_Selected_Signal = Signal(Path)

    def __init__(self):
        super(RecentProjectsWidget, self).__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.top_label = QLabel(text='Открытые ранее проекты:')
        self.top_label.setFont(QFont('Arial', 12))
        layout.addWidget(self.top_label)

        self.list = QListWidget()

        self.list.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerItem)

        layout.addWidget(self.list)
        self.list.itemClicked.connect(self._on_item_clicked)
        pass

    def set_project_paths(self, project_paths: list):
        self.list.clear()
        for path in project_paths:
            el = LoadedQListWidgetItem(path, str(path))
            el.setFont(QFont('Arial', 15))
            self.list.addItem(el)
        pass

    def _on_item_clicked(self, item: LoadedQListWidgetItem):
        self.Project_Selected_Signal.emit(item.payload)
        pass

    pass
