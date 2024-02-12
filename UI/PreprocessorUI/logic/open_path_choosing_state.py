from UI.PreprocessorUI.logic.app_state_base import AppStateBase
from UI.PreprocessorUI.widgets.path_choosing_widget import PathChoosingWidget
from pathlib import Path
from PySide6.QtCore import Signal


class OpenPathChoosingState(AppStateBase):
    Return_Signal = Signal()
    Path_Chosen = Signal(Path)

    def __init__(self):
        super().__init__()
        self.main_widget = PathChoosingWidget(
            'please select existing project folder',
            default_feedback='some default feedback'
        )
        self.main_widget.Something_Inputted_As_Path.connect(
            self._verify_path
        )
        self.main_widget.Continue_Signal.connect(
            self._open_and_proceed
        )
        self.main_widget.Return_Signal.connect(
            lambda: self.Return_Signal.emit()
        )
        pass

    def get_main_widget(self):
        return self.main_widget

    def transfer_control(self):
        self.Show_Main_Widget.emit(self.get_main_widget())
        pass

    def _verify_path(self, user_input_path):
        # todo: add verification here too
        self.main_widget.enable_continue_button()
        pass

    def _open_and_proceed(self, user_input_path: str):
        path = Path(user_input_path)
        self.Path_Chosen.emit(path)
    pass
