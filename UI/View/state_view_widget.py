from PySide6.QtWidgets import QWidget, QStackedLayout
from UI.BeginningScreen.select_project_opening_option_state import SelectProjectOpeningOptionState
from UI.BeginningScreen.create_new_project_option_state import CreateNewProjectOptionState
from UI.BeginningScreen.open_existing_project_option_state import OpenExistingProjectOptionState
from UI.ProjectControlScreen.project_control_state import ProjectControlState
from UI.app_state_base import AppStateBase
from UI.MainScreen.logic.descriptor_state import DescriptorState


class StateViewWidget(QWidget):
    def __init__(self):
        super(StateViewWidget, self).__init__()
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        self.open_or_create_state = SelectProjectOpeningOptionState()
        self._configure_state(self.open_or_create_state)
        self.create_path_choosing_state = CreateNewProjectOptionState()
        self._configure_state(self.create_path_choosing_state)
        self.open_path_choosing_stata = OpenExistingProjectOptionState()
        self._configure_state(self.open_path_choosing_stata)
        self.project_control_state = ProjectControlState()
        self._configure_state(self.project_control_state)
        self._descriptor_state = DescriptorState()
        self._configure_state(self._descriptor_state)

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
            self._descriptor_state.transfer_control
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
