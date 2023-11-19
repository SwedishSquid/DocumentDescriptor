import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication()
    main_window = MainWindow()
    main_window.showMaximized()
    app.setWindowIcon(QIcon(os.path.join("resources", "file.svg")))
    app.exec()
