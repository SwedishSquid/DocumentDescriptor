from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, \
    QTextEdit

from domain.statistics import Statistics
from PySide6.QtCore import Signal


class ProjectStatisticsWidget(QWidget):
    Reload_Statistics_Signal = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.path_text_edit = QTextEdit()
        self.path_text_edit.setReadOnly(True)
        layout.addWidget(self.path_text_edit)

        self.label = QLabel()
        layout.addWidget(self.label)

        m = 'reload'
        m_rus = 'Обновить статистику по проекту'
        self.reload_button = QPushButton(text=m_rus)
        layout.addWidget(self.reload_button)
        self.reload_button.clicked.connect(lambda: self.Reload_Statistics_Signal.emit())
        pass

    def set_statistics(self, stats: Statistics):
        message_list = [
            f'в корне найдено {stats.books_in_source_count} книг',
            f'из них предобработанно {stats.preprocessed_books_count} штук',
            f'осталось предобработать {stats.left_to_preprocess_books_count} штук',
            f'',
            f'состояние предобработанных книг:',
            f'закончено {stats.finished_books_count} книг',
            f'отклонено {stats.rejected_books_count} книг',
            f'начато описание {stats.in_progress_books_count} книг',
            f'описание не начато для {stats.not_started_books_count} книг']

        self.label.setText('\n'.join(message_list))
        self.path_text_edit.setText(str(stats.project_path))
        pass
    pass

