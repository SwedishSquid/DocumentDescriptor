from PySide6.QtWidgets import QWidget, QStackedLayout
from UI.PreprocessorUI.logic.open_or_create_state import OpenOrCreateState
from UI.PreprocessorUI.logic.create_path_choosing_state import CreatePathChoosingState
from UI.PreprocessorUI.logic.open_path_choosing_state import OpenPathChoosingState
from UI.PreprocessorUI.logic.project_control_state import ProjectControlState
from UI.PreprocessorUI.logic.app_state_base import AppStateBase


class StateViewWidget(QWidget):
    def __init__(self):
        super(StateViewWidget, self).__init__()
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        self.open_or_create_state = OpenOrCreateState()
        self._configure_state(self.open_or_create_state)
        self.create_path_choosing_state = CreatePathChoosingState()
        self._configure_state(self.create_path_choosing_state)
        self.open_path_choosing_stata = OpenPathChoosingState()
        self._configure_state(self.open_path_choosing_stata)
        self.project_control_state = ProjectControlState()
        self._configure_state(self.project_control_state)

        self.open_or_create_state.Create_New_Project.connect(
            self.create_path_choosing_state.transfer_control
        )
        self.open_or_create_state.Open_Existing_Project.connect(
            self.open_path_choosing_stata.transfer_control
        )

        self.create_path_choosing_state.Path_Chosen.connect(
            self.project_control_state.transfer_control
        )
        self.create_path_choosing_state.Return_Signal.connect(
            self.open_or_create_state.transfer_control
        )

        self.open_path_choosing_stata.Path_Chosen.connect(
            self.project_control_state.transfer_control
        )
        self.open_path_choosing_stata.Return_Signal.connect(
            self.open_or_create_state.transfer_control
        )

        self.project_control_state.Open_Descriptor.connect(
            lambda p: print(f'open descriptor at {p} please')
        )
        self.project_control_state.Return_Signal.connect(
            self.open_or_create_state.transfer_control
        )

        self.open_or_create_state.transfer_control()
        pass

    def _configure_state(self, state: AppStateBase):
        self.layout.addWidget(state.get_main_widget())
        state.Show_Main_Widget.connect(self._set_current_widget)
        pass

    def _set_current_widget(self, widget: QWidget):
        self.layout.setCurrentWidget(widget)
        pass
    pass
