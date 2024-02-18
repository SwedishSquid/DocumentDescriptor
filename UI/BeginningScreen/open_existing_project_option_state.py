from UI.app_state_base import AppStateBase
from UI.BeginningScreen.widgets.path_choosing_widget import PathChoosingWidget
from pathlib import Path
from PySide6.QtCore import Signal
from domain.submodules.project_folder_manager import ProjectFolderManager


class OpenExistingProjectOptionState(AppStateBase):
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
        manager = self._try_open_project(
            user_input_path,
            ms_receiver=self.main_widget.set_feedback_string)
        if manager is not None:
            self.main_widget.enable_continue_button()
        pass

    def _try_open_project(self, user_input_path: str, ms_receiver=None):
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
        if not path.is_dir():
            ms_receiver('path must point at an existing project directory')
            return
        # todo: check if it is a good way of testing for project folder
        manager = ProjectFolderManager.load_from_path(path)
        if manager is None:
            ms_receiver('not a valid project')
            return
        ms_receiver('project found')
        return manager

    def _open_and_proceed(self, user_input_path: str):
        path = Path(user_input_path)
        self.Path_Chosen.emit(path)
    pass
