from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, \
    QHBoxLayout

from domain.statistics import Statistics
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, Qt
from UI.resizable_qtextedit import ResizableTextEdit


class ProjectStatisticsWidget(QWidget):
    Reload_Statistics_Signal = Signal()

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.path_text_edit = self._make_path_text_edit()
        main_layout.addWidget(self.path_text_edit)

        secondary_layout = QHBoxLayout()
        main_layout.addLayout(secondary_layout)

        self.stats_label = self._make_stats_label()
        secondary_layout.addWidget(self.stats_label,
                                   alignment=Qt.AlignmentFlag.AlignCenter)

        m = 'reload'
        m_rus = 'Обновить статистику по проекту'
        self.refresh_button = self._make_refresh_button(m_rus)
        secondary_layout.addWidget(self.refresh_button,
                                   alignment=Qt.AlignmentFlag.AlignLeft)
        self.refresh_button.clicked.connect(self.Reload_Statistics_Signal.emit)
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

        self.stats_label.setText('\n'.join(message_list))
        self.path_text_edit.setText(str(stats.project_path))
        pass

    def _make_path_text_edit(self):
        te = ResizableTextEdit()
        te.setFont(QFont('Arial', 12))
        te.setReadOnly(True)
        te.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # te.setAlignment(Qt.AlignmentFlag.AlignTop)
        return te

    def _make_stats_label(self):
        label = QLabel()
        label.setFont(QFont('Arial', 12))
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # label.setTextFormat()
        return label

    def _make_refresh_button(self, text):
        b = QPushButton(text=text)
        b.setFont(QFont('Arial', 12))
        # b.setSizePolicy(QSizePolicy.Policy.Minimum,
        #                 QSizePolicy.Policy.Maximum)
        b.setFixedSize(300, 100)
        return b
    pass

