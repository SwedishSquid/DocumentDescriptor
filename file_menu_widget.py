import PySide6.QtCore
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from select_location_widget import SelectLocationWidget


class FileMenuWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.select_file_location_widget = SelectLocationWidget(True)
        self.select_folder_location_widget = SelectLocationWidget(False)
        self.layout().addWidget(self.select_file_location_widget)
        self.layout().addWidget(self.select_folder_location_widget)
        self.layout().setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignHCenter)
