from UI.app_state_base import AppStateBase
from UI.ProjectControlScreen.project_control_widget import ProjectControlWidget
from UI.ProjectControlScreen.preprocess_dialog.preprocess_dialog import PreprocessDialog
from pathlib import Path
from PySide6.QtCore import Signal
from domain.glue import Glue
from threading import Thread


class ProjectControlState(AppStateBase):
    Open_Descriptor = Signal(Path)
    Return_Signal = Signal()

    def __init__(self):
        super().__init__()
        self.main_widget = ProjectControlWidget()
        self.main_widget.Start_Preprocessing_Signal.connect(
            self._start_preprocessing
        )
        self.main_widget.Open_Main_App_Signal.connect(
            lambda: self.Open_Descriptor.emit(self.project_path)
        )
        self.main_widget.Export_Signal.connect(
            self._start_exporting
        )
        # todo: add return option

        self.preprocess_dialog = PreprocessDialog()

        self.project_path: Path = None
        pass

    def get_main_widget(self):
        return self.main_widget

    def transfer_control(self, project_path: Path):
        # todo: check if path is valid
        self.project_path = project_path
        self.Show_Main_Widget.emit(self.get_main_widget())
        pass

    def _start_preprocessing(self):
        # todo: protect against multiple calls
        def ms_receiver(s: str):
            self.preprocess_dialog.add_output_text(s)
            pass

        glue = Glue(self.project_path)

        def func_to_thread():
            for done, total in glue.get_preprocessor_generator(
                    ms_receiver=ms_receiver):
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

    def _start_exporting(self):
        print('exporting not available yet')
        # todo: make exporting
        pass

    pass
