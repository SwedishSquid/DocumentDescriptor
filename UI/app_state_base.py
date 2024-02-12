import abc
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QWidget


class AppStateBase(QObject):
    Show_Main_Widget = Signal(QWidget)

    @abc.abstractmethod
    def get_main_widget(self):
        pass
