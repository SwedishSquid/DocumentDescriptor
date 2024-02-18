from UI.app_state_base import AppStateBase
from UI.ProjectControlScreen.project_control_widget import ProjectControlWidget
from UI.ProjectControlScreen.preprocess_dialog.preprocess_dialog import PreprocessDialog
from pathlib import Path
from PySide6.QtCore import Signal
from domain.glue import Glue
from threading import Thread
from domain.statistics import Statistics
import multiprocessing as mp
import time
from collections import namedtuple


ProcessOutputMessage = namedtuple('ProcessOutputMessage', 'type payload')


def _multiprocess_target(output_queue: mp.Queue, stop_when_cant_preprocess: bool,
                         project_path: Path):
    def ms_receiver(s: str, ms_type=None):
        if ms_type is None:
            ms_type = 'info'
        output_queue.put(ProcessOutputMessage(type=ms_type, payload=s))
        pass
    generator, total_book_count = Glue(project_path).get_preprocessor_generator()
    completed_count = 0
    for completed_book_preprocessing in generator:
        completed_count += 1
        ms_receiver(f'!!! done {completed_count} out of {total_book_count} !!!')
        if not completed_book_preprocessing.success:
            ms_receiver(
                f'cant preprocess book at {completed_book_preprocessing.original_book_path}')
            if stop_when_cant_preprocess:
                ms_receiver(
                    'stopping cause configured to stop when cant preprocess')
                break
            else:
                pass
                ms_receiver(
                    'skipped that book cause configured to skip when cant preprocess')
    ms_receiver('preprocessing finished; window can be closed', ms_type='main_message')
    ms_receiver('', ms_type='fin')
    pass


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
        self.main_widget.Refresh_Statistics.connect(
            self._refresh_statistics
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
        self._refresh_statistics()
        self.Show_Main_Widget.emit(self.get_main_widget())
        pass

    def _refresh_statistics(self):
        stats = Statistics.make_statistics_from_project_path(self.project_path)
        self.main_widget.statistics_widget.set_statistics(stats)
        pass

    def _start_preprocessing(self):
        # todo: protect against multiple calls
        def ms_receiver(s: str):
            self.preprocess_dialog.add_output_text(s)
            pass

        # todo: cleanup this mess

        glue = Glue(self.project_path)

        message_queue = mp.Queue()
        process = mp.Process(target=_multiprocess_target,
                             args=(message_queue,
                                   glue.get_project_manager().config.stop_when_cant_preprocess,
                                   self.project_path))
        process.start()

        def thread_target():
            while True:
                if not message_queue.empty():
                    message: ProcessOutputMessage = message_queue.get()
                    if message.type == 'info':
                        ms_receiver(message.payload)
                    elif message.type == 'fin':
                        break
                    else:
                        self.preprocess_dialog.set_message(message.payload)
                else:
                    print('nothing to do')
                    time.sleep(0.01)
            pass
        message_getter_thread = Thread(target=thread_target)
        message_getter_thread.start()

        print('preprocessing started')
        self.preprocess_dialog.set_message('preprocessing started; do not close window until preprocessing finished')
        self.preprocess_dialog.exec()
        if process.is_alive():
            # todo: do something to stop it
            print('process is still active. please wait')
            process.kill()
            print('process was killed; might cause some issues. in that case reboot app')
        message_queue.put(ProcessOutputMessage(type='fin', payload=''))
        print('preprocessing finished')
        pass

    def _start_exporting(self):
        print('exporting started')
        exporter = Glue(self.project_path).get_exporter()
        exporter.export_finished_books()
        exporter.export_rejected_books()
        print('exporting finished')
        pass
    pass
