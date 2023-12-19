from UI.constant_paths import path_to_pictures
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from UI.BeginningScreen.beginning_window import BeginningWindow
from UI.MainScreen.main_window import MainWindow
from UI.View.view import View

if __name__ == "__main__":
    # app = QApplication()
    # main_window = BeginningWindow()
    # # main_window = MainWindow()
    # main_window.showMaximized()
    # app.setWindowIcon(QIcon(str(path_to_pictures.joinpath('file'))))
    # app.exec()
    view = View()
    view.run()
