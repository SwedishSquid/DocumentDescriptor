from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class PDFViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.document = QPdfDocument()
        # self.document.load(r"C:\Users\Евгений\Downloads\lib\lib\Только image.Райзер Герберт Дж. Комбинаторная математика.pdf")
        view = QPdfView()
        view.setPageMode(QPdfView.PageMode.MultiPage)
        view.setDocument(self.document)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(view)
