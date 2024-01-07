from PySide6.QtCore import QSize, QRect, QPointF, QRectF, QSizeF, QMargins
from PySide6.QtGui import QPolygonF
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QRubberBand, QSizePolicy
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class PDFViewer(QPdfView):
    def __init__(self):
        super().__init__()

        self.rect = None
        self.origin = None
        self.rubber_band = None
        self.selected_bands = []
        self.document = QPdfDocument()
        self.setPageMode(QPdfView.PageMode.SinglePage)
        self.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.setDocumentMargins(QMargins(0, 0, 0, 0))
        self.setDocument(self.document)

        # self.setLayout(QVBoxLayout())
        # self.message_widget = QPlainTextEdit()
        # self.message_widget.setReadOnly(True)
        # self.layout().addWidget(self.message_widget)

    def mousePressEvent(self, event):
        if len(self.selected_bands) > 0:
            for b in self.selected_bands:
                b.deleteLater()
            self.selected_bands = []
        self.origin = event.pos()
        if self.rubber_band is None:
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()

    def mouseMoveEvent(self, event):
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        msg = ""
        self.rect = QRectF(self.origin, event.pos()).normalized()
        self.rubber_band.hide()

        pdf_selection = self.document.getAllText(0)
        bounds = pdf_selection.bounds()

        selected_bounds = list(filter(self.filter_overlapped_bounds, bounds))
        for b in selected_bounds:
            doc_margins = self.documentMargins()
            shift = QPointF(doc_margins.left(), doc_margins.top())
            rubber_band = QRubberBand(QRubberBand.Rectangle, self)
            rect = b.boundingRect()
            zoom = self.width() / self.document.pagePointSize(0).width()
            view_rect = QRect((rect.topLeft() * zoom + shift).toPoint(),
                              (rect.bottomRight() * zoom + shift).toPoint())
            rubber_band.setGeometry(view_rect)
            rubber_band.show()
            self.selected_bands.append(rubber_band)


        selection = self.document.getSelection(0, selected_bounds[0].boundingRect().topLeft(),
                                               selected_bounds[-1].boundingRect().bottomRight())
        # print(selection.isValid())
        print(selection.text())
        # print(msg)

    def filter_overlapped_bounds(self, bound: QPolygonF):
        doc_margins = self.documentMargins()
        shift = QPointF(doc_margins.left(), doc_margins.top())
        unshifted_view_rect = QRectF(self.rect.topLeft() + shift,
                                     QSizeF(self.rect.width(), self.rect.height()))
        zoom = self.width() / self.document.pagePointSize(0).width()
        pdf_rect = QRectF((unshifted_view_rect.topLeft() / zoom),
                          (unshifted_view_rect.bottomRight() / zoom))
        if pdf_rect.intersects(bound.boundingRect()):
            return True
        return False

    def set_document(self, path: str):
        self.document.load(str(path))
