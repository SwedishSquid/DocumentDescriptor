from UI.app_state_base import AppStateBase
from UI.ProjectControlScreen.project_control_widget import ProjectControlWidget
from UI.ProjectControlScreen.preprocess_dialog.preprocess_dialog import PreprocessDialog
from pathlib import Path
from PySide6.QtCore import Signal
from domain.glue import Glue
from threading import Thread, Event
from domain.statistics import Statistics
from UI.helpers.inform_dialog import InformDialog
import logging
from domain.submodules.previous_projects_storage_manager import PreviousProjectsStorageManager


class ProjectControlState(AppStateBase):
    Open_Descriptor = Signal(Path)
    Return_Signal = Signal()
    _Add_Text_To_Preprocess_Dialog = Signal(str)
    _Change_Message_At_Preprocess_Dialog = Signal(str)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        self.main_widget = ProjectControlWidget()
        self.main_widget.Start_Preprocessing_Signal.connect(
            self._action_trigger_decorator(self._start_preprocessing)
        )
        self.main_widget.Open_Main_App_Signal.connect(
            lambda: self.Open_Descriptor.emit(self.project_path)
        )
        self.main_widget.Export_Signal.connect(
            self._action_trigger_decorator(self._start_exporting)
        )
        self.main_widget.Refresh_Statistics.connect(
            self._refresh_statistics
        )
        # todo: add return option

        self.preprocess_dialog = PreprocessDialog()

        self._Add_Text_To_Preprocess_Dialog.connect(self.preprocess_dialog.add_output_text)
        self._Change_Message_At_Preprocess_Dialog.connect(self.preprocess_dialog.set_message)

        self.project_path: Path = None

        self._can_start_actions = True      # to prevent user from starting several actions at once
        pass

    def get_main_widget(self):
        return self.main_widget

    def transfer_control(self, project_path: Path):
        # todo: check if path is valid
        self.project_path = project_path
        self._refresh_statistics()
        self.Show_Main_Widget.emit(self.get_main_widget())
        self.main_widget.set_enabled_for_all_action_buttons(True)
        PreviousProjectsStorageManager().update_projects_list(self.project_path)
        pass

    def _enable_all_actions(self):
        self._can_start_actions = True
        self.main_widget.set_enabled_for_all_action_buttons(True)
        pass

    def _disable_all_actions(self):
        self._can_start_actions = False
        self.main_widget.set_enabled_for_all_action_buttons(False)
        pass

    def _action_trigger_decorator(self, action_trigger_func):
        def inner_func(*args, **kwargs):
            self._disable_all_actions()
            action_trigger_func(*args, **kwargs)
            self._enable_all_actions()
            pass
        return inner_func

    def _refresh_statistics(self):
        stats = Statistics.make_statistics_from_project_path(self.project_path)
        self.main_widget.statistics_widget.set_statistics(stats)
        pass

    def _start_preprocessing(self):
        # todo: protect against multiple calls
        # fixme: what a mess
        self.logger.debug('start preprocessing')

        def ms_receiver(s: str):
            # do it thread safe
            self._Add_Text_To_Preprocess_Dialog.emit(s)
            pass

        def set_operation_status_message(s: str):
            self._Change_Message_At_Preprocess_Dialog.emit(s)
            pass

        glue = Glue(self.project_path)
        stop_event = Event()

        def func_to_thread():
            generator, total_book_count = glue.get_preprocessor_generator()
            completed_count = 0
            for completed_book_preprocessing in generator:
                if stop_event.is_set():
                    break
                completed_count += 1
                m = f'!!! done {completed_count} out of {total_book_count} !!!'
                m_rus = f'!!! Сделано {completed_count} из {total_book_count} !!!'
                ms_receiver(m_rus)
                if not completed_book_preprocessing.success:
                    m = f'cant preprocess book at {completed_book_preprocessing.original_book_path}'
                    m_rus = f'Не получается предобработать книгу {completed_book_preprocessing.original_book_path}'
                    ms_receiver(m_rus)
                    if glue.get_project_manager().config.stop_when_cant_preprocess:
                        m = 'stopping cause configured to stop when cant preprocess'
                        m_rus = 'Предобработка прервана, т.к. в настройках (в конфиге) указано останавливаться когда не получается предобработать документ'
                        ms_receiver(m_rus)
                        break
                    else:
                        pass
                        m = 'skipped that book cause configured to skip when cant preprocess'
                        m_rus = 'Документ, который не удалось предобработать, пропущен. (такие вот настройки)'
                        ms_receiver(m_rus)
            m = 'preprocessing finished'
            m_rus = 'Предобработка завершена'
            set_operation_status_message(m_rus)
            pass

        thread = Thread(target=func_to_thread)
        thread.start()

        m = 'do not close until preprocessing finished'
        m_rus = 'Пожалуйста, не закрывайте это окно до окончания предобработки'
        set_operation_status_message(m_rus)
        # print('preprocessing started')
        self.preprocess_dialog.exec()
        if thread.is_alive():
            stop_event.set()
            self._run_stop_preprocessing_dialog_and_wait_for_thread_termination(thread)
        else:
            pass
        # print('preprocessing finished')
        self.logger.debug('finish preprocessing')
        pass

    def _run_stop_preprocessing_dialog_and_wait_for_thread_termination(self, thread: Thread):
        info_dialog = InformDialog()

        def _inform_when_finished():
            thread.join()
            m_rus = 'Предобработка успешно прервана. Это окно можно закрывать'
            info_dialog.set_info_message_thread_safe(m_rus)
            pass

        m_rus = 'Прерывание предобработки. Ждем окончания предобработки текущей книги. Закрытие этого окна может привести к зависанию программы'
        info_dialog.set_info_message_thread_safe(m_rus)

        dialog_thread = Thread(target=_inform_when_finished)
        dialog_thread.start()
        info_dialog.exec()
        dialog_thread.join()
        pass

    def _start_exporting(self):
        print('exporting started')
        inform_dialog = InformDialog()
        m = 'export started; please do not close this window'
        m_rus = 'Экспорт данных начат, Не закрывайте это окно'
        inform_dialog.set_info_message_thread_safe(m_rus)

        def _export():
            exporter = Glue(self.project_path).get_exporter()
            exporter.export_finished_books()
            exporter.export_rejected_books()
            m = 'export finished; this window can be closed now'
            m_rus = 'Экспорт данных завершен. Окно может быть закрыто'
            inform_dialog.set_info_message_thread_safe(m_rus)
            pass

        thread = Thread(target=_export)
        thread.start()

        inform_dialog.exec()
        thread.join()
        print('exporting finished')
        pass
    pass
