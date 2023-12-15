from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class PDFViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.document = QPdfDocument()
        # self.document.load(r"C:\Users\Евгений\Downloads\lib\lib\Только image.Райзер Герберт Дж. Комбинаторная математика.pdf")
        self.view = QPdfView()
        self.view.setPageMode(QPdfView.PageMode.MultiPage)
        self.view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.view.setDocument(self.document)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.view)

    def set_document(self, path: str):
        self.document.load(str(path))
