from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView  # , QWebEngineSettings
from os import path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Viewer")
        self.setGeometry(0, 28, 1000, 750)

        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(
            self.webView.settings().WebAttribute.PluginsEnabled, True)
        self.webView.settings().setAttribute(
            self.webView.settings().WebAttribute.PdfViewerEnabled, True)
        self.setCentralWidget(self.webView)

    def url_changed(self):
        self.setWindowTitle(self.webView.title())

    def go_back(self):
        self.webView.back()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    if len(sys.argv) > 1:
        win.webView.setUrl(QUrl(f"file://{sys.argv[1]}"))
    else:
        wd = path.dirname(path.abspath(sys.argv[0]))
        print(f"wd: {wd}")
        path = "E:/dev/DocumentDescriptor/DocumentDescriptor/dir_that_git_ignores/2/test.pdf"
        url_str = f"file://{path}"
        print(url_str)
        url = QUrl.fromLocalFile(path)
        win.webView.setUrl(url)
    sys.exit(app.exec())
