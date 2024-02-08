from PySide6.QtWidgets import QDialog, QVBoxLayout
from UI.MainScreen.book_list import BookList
from domain.engine import FullListRecord


class FullBookList(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Полный список книг")
        self.resize(800, 600)

        self.book_list = BookList(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.book_list)
        self.accepted.connect(self.view.save_book_meta_as_in_progress)

    # def run(self):
    #     self.exec()

    def run_dialog(self, book_records: list):
        self.book_list.clear()
        for i in range(len(book_records)):
            record: FullListRecord = book_records[i]
            self.book_list.add_book(
                i,
                str(record.rel_path.name),
                record.descr_stage
            )
        self.exec()
        pass
