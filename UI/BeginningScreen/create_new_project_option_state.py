from UI.app_state_base import AppStateBase
from UI.BeginningScreen.widgets.path_choosing_widget import PathChoosingWidget
from pathlib import Path
from PySide6.QtCore import Signal
from domain.glue import Glue


class CreateNewProjectOptionState(AppStateBase):
    Return_Signal = Signal()
    Path_Chosen = Signal(Path)

    def __init__(self):
        super().__init__()
        self.main_widget = PathChoosingWidget(
            'please select folder in which project files will be stored',
            default_feedback='some feedback')
        self.main_widget.Something_Inputted_As_Path.connect(
            self._verify_path
        )
        self.main_widget.Continue_Signal.connect(
            self._create_project_and_proceed
        )
        self.main_widget.Return_Signal.connect(
            lambda: self.Return_Signal.emit()
        )
        pass

    def get_main_widget(self):
        return self.main_widget

    def transfer_control(self):
        self.main_widget.clear_input_text()
        self.Show_Main_Widget.emit(self.get_main_widget())
        pass

    def _verify_path(self, user_input_path: str):
        path = self._try_parse_path(user_input_path, self.main_widget.set_feedback_string)
        if not path is None:
            self.main_widget.enable_continue_button()
        pass

    def _try_parse_path(self, user_input_path: str, ms_receiver=None):
        # todo: check if directory contains any files
        # todo: remove logic from UI layer
        if ms_receiver is None:
            ms_receiver = lambda s: None
        try:
            path = Path(user_input_path)
        except Exception as e:
            ms_receiver(str(e))
            return
        if not path.is_absolute():
            ms_receiver('path must be absolute')
            return
        if path.is_file():
            ms_receiver('path must represent a folder, not a file')
            return
        ms_receiver(f'project files will be located at {path}')
        return path

    def _create_project_and_proceed(self):
        path = self._try_parse_path(self.main_widget.get_input_text())
        if path is None:
            # todo: handle this situation
            print('invalid path')
            return
        Glue(path).init_project()
        self.Path_Chosen.emit(path)
    pass
