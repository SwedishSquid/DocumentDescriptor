from UI.PreprocessorUI.logic.app_state_base import AppStateBase
from UI.PreprocessorUI.widgets.open_or_create_widget import OpenOrCreateWidget
from PySide6.QtCore import Signal


class OpenOrCreateState(AppStateBase):
    Create_New_Project = Signal()
    Open_Existing_Project = Signal()

    def __init__(self):
        super().__init__()
        self.main_widget = OpenOrCreateWidget()
        self.main_widget.Create_New_Project_Signal.connect(
            lambda: self.Create_New_Project.emit()
        )
        self.main_widget.Open_Existing_Project_Signal.connect(
            lambda: self.Open_Existing_Project.emit()
        )
        pass

    def get_main_widget(self):
        return self.main_widget

    def transfer_control(self):
        # todo: reload recent projects list
        self.Show_Main_Widget.emit(self.get_main_widget())
        pass
    pass
