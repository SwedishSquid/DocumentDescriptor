from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow
from pathlib import Path


class BrowserPdfViewer(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.settings().setAttribute(
            self.settings().WebAttribute.PluginsEnabled, True)
        self.settings().setAttribute(
            self.settings().WebAttribute.PdfViewerEnabled, True)
        pass

    def set_file(self, path: Path):
        url = QUrl.fromLocalFile(path)
        self.setUrl(url)
        pass
    pass


if __name__ == '__main__':
    import sys
    app = QApplication()
    win = QMainWindow()
    win.setGeometry(0, 28, 1000, 750)
    pdf_viewer = BrowserPdfViewer()
    win.setCentralWidget(pdf_viewer)
    win.show()
    file = Path("E:/dev/DocumentDescriptor/DocumentDescriptor/dir_that_git_ignores/2/test.pdf")
    pdf_viewer.set_file(file)
    sys.exit(app.exec())
