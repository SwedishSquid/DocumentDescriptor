from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
    QLabel, QStackedWidget, QStackedLayout
from PySide6.QtCore import Signal
from pathlib import Path

from UI.PreprocessorUI.open_or_create_widget import OpenOrCreateWidget
from UI.PreprocessorUI.path_choosing_widget import PathChoosingWidget
from UI.PreprocessorUI.project_control_widget import ProjectControlWidget
from UI.PreprocessorUI.preprocess_dialog.preprocess_dialog import PreprocessDialog
from domain.preprocessor import Preprocessor
from domain.submodules.project_folder_manager import ProjectFolderManager
from threading import Thread
from domain.glue import Glue


class PreprocessorWidget(QWidget):
    # todo: how about sending not path but project manager?
    Open_Descriptor_Signal = Signal(Path)

    def __init__(self):
        super(PreprocessorWidget, self).__init__()
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        self.open_or_create_widget = self._init_open_or_create_widget()
        self.layout.addWidget(self.open_or_create_widget)

        self.path_choosing_to_create_new_project_widget \
            = self._init_path_choosing_to_create_new_project_widget()
        self.layout.addWidget(self.path_choosing_to_create_new_project_widget)

        self.path_choosing_to_open_existing_project_widget \
            = self._init_path_choosing_to_open_existing_project_widget()
        self.layout.addWidget(self.path_choosing_to_open_existing_project_widget)

        self.project_control_widget = self._init_project_control_widget()
        self.layout.addWidget(self.project_control_widget)

        self.preprocess_dialog = PreprocessDialog()

        # self.current_project_path: Path = None

        # self.project_folder_manager: ProjectFolderManager = None
        self.glue: Glue = None
        pass

    # region init methods
    def _init_open_or_create_widget(self):
        widget = OpenOrCreateWidget()
        widget.Create_New_Project_Signal.connect(
            self._on_create_new_project_option)
        widget.Open_Existing_Project_Signal.connect(
            self._on_open_existing_project_option
        )
        return widget

    def _init_path_choosing_to_create_new_project_widget(self):
        widget = PathChoosingWidget(
            'please select folder in which project files will be stored',
            default_feedback='some feedback')
        widget.Continue_Signal.connect(
            self._create_new_project_and_proceed
        )
        widget.Return_Signal.connect(
            self._return_to_open_or_create_widget
        )
        widget.Something_Inputted_As_Path.connect(
            self._path_verification_for_new_project_creation
        )
        return widget

    def _init_path_choosing_to_open_existing_project_widget(self):
        widget = PathChoosingWidget('please select existing project folder',
                                    default_feedback='feedback on existing project')
        widget.Continue_Signal.connect(
            self._open_existing_project_and_proceed
        )
        widget.Return_Signal.connect(
            self._return_to_open_or_create_widget
        )
        widget.Something_Inputted_As_Path.connect(
            self._path_verification_to_open_existing_project
        )
        return widget

    def _init_project_control_widget(self):
        widget = ProjectControlWidget()
        widget.Start_Preprocessing_Signal.connect(
            self._start_preprocessing
        )
        widget.Open_Main_App_Signal.connect(
            self._open_main_app
        )
        widget.Export_Signal.connect(
            self._export_data
        )
        return widget
    # endregion init methods

    # region private slots
    def _on_create_new_project_option(self):
        self.layout.setCurrentWidget(
            self.path_choosing_to_create_new_project_widget)
        pass

    def _on_open_existing_project_option(self):
        self.layout.setCurrentWidget(
            self.path_choosing_to_open_existing_project_widget
        )
        pass

    def _return_to_open_or_create_widget(self):
        self.layout.setCurrentWidget(
            self.open_or_create_widget
        )
        pass

    def _path_verification_for_new_project_creation(self,  user_input_path: str):
        try:
            path = Path(user_input_path)
        except Exception as e:
            self.path_choosing_to_create_new_project_widget.set_feedback_string(str(e))
            return
        if not path.is_absolute():
            self.path_choosing_to_create_new_project_widget.set_feedback_string('path must be absolute')
            return
        if path.is_file():
            self.path_choosing_to_create_new_project_widget.set_feedback_string('path must represent a folder, not a file')
            return
        self.path_choosing_to_create_new_project_widget.set_feedback_string(str(path))
        self.path_choosing_to_create_new_project_widget.enable_continue_button()
        pass

    def _path_verification_to_open_existing_project(self, user_input_path: str):
        # todo: add verification here too

        self.path_choosing_to_open_existing_project_widget.enable_continue_button()
        pass

    def _create_new_project_and_proceed(self, pathlike: str):
        # todo: check if directory contains any files
        # todo: check if pathlike is valid path
        path = Path(pathlike)
        ProjectFolderManager.init_project(path)
        self._activate_project_control_widget(path)
        pass

    def _open_existing_project_and_proceed(self, pathlike: str):
        # todo: check if valid project
        path = Path(pathlike)
        self._activate_project_control_widget(path)
        pass

    def _start_preprocessing(self):
        # todo: protect against multiple calls
        def ms_receiver(s: str):
            self.preprocess_dialog.add_output_text(s)
            pass

        def func_to_thread():
            for done, total in self.glue.get_preprocessor_generator(ms_receiver=ms_receiver):
                ms_receiver(f'!!! done {done} out of {total} !!!')
            pass
        thread = Thread(target=func_to_thread)
        thread.start()
        print('preprocessing started')
        self.preprocess_dialog.exec()
        if thread.is_alive():
            # todo: do something to stop it
            print('thread is still active. please wait')
            thread.join()
        print('preprocessing finished')
        pass

    def _open_main_app(self):
        # todo: resend signal
        print('open it already')
        pass

    def _export_data(self):
        print('exporting data :D')
        pass

    def _activate_project_control_widget(self, path: Path):
        # todo: check if successful
        self.glue = Glue(path)
        self.layout.setCurrentWidget(
            self.project_control_widget
        )
        pass
    # endregion private slots
    pass
