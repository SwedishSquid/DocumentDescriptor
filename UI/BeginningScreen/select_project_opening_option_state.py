from UI.app_state_base import AppStateBase
from UI.BeginningScreen.widgets.open_create_recent_widget import OpenCreateRecentWidget
from PySide6.QtCore import Signal
from pathlib import Path
from domain.glue import Glue
from UI.helpers.inform_dialog import InformDialog


class SelectProjectOpeningOptionState(AppStateBase):
    Create_New_Project = Signal()
    Open_Existing_Project = Signal()
    Open_Recent_Project = Signal(Path)

    def __init__(self):
        super().__init__()
        self.main_widget = OpenCreateRecentWidget()
        self.main_widget.Create_New_Project_Signal.connect(
            lambda: self.Create_New_Project.emit()
        )
        self.main_widget.Open_Existing_Project_Signal.connect(
            lambda: self.Open_Existing_Project.emit()
        )
        self.main_widget.Open_Recent_Project_Signal.connect(
            self._on_recent_project_selected
        )

        # self.main_widget.set_recent_projects([Path(r'E:\ProjectLib\result_root')])
        pass

    def get_main_widget(self):
        return self.main_widget

    def transfer_control(self):
        # todo: reload recent projects list
        self.Show_Main_Widget.emit(self.get_main_widget())
        pass

    def _on_recent_project_selected(self, path: Path):
        if Glue(path).init_happened():
            self.Open_Recent_Project.emit(path)
        else:
            dialog = InformDialog()
            dialog.set_info_message_thread_safe('Проект не найден.\nПопробуйте открыть его через опцию "Открыть"')
            dialog.exec()
    pass
