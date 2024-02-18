from UI.app_state_base import AppStateBase
from UI.BeginningScreen.widgets.path_choosing_widget import PathChoosingWidget
from pathlib import Path
from PySide6.QtCore import Signal
from domain.glue import Glue


class OpenExistingProjectOptionState(AppStateBase):
    Return_Signal = Signal()
    Path_Chosen = Signal(Path)

    def __init__(self):
        super().__init__()
        m = 'please select existing project folder'
        m_rus = 'Пожалуйста, выберите существующую папку проекта (ранее созданный проект)'
        self.main_widget = PathChoosingWidget(
            m_rus,
            return_button_text='Назад',
            input_field_hint='Вводить путь здесь (можно еще выбрать в проводнике кнопкой справа)',
            continue_button_text='Продолжить',
            default_feedback='Здесь отобразится, подходит ли выбранная папка'
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
        res = self._try_open_project(
            user_input_path,
            ms_receiver=self.main_widget.set_feedback_string)
        if res:
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
            m = 'path must be absolute'
            m_rus = 'Папка не подходит. Путь должен быть абсолютным (начинаться с буквы диска. Например E:/...'
            ms_receiver(m_rus)
            return
        if not path.is_dir():
            m = 'path must point at an existing project directory'
            m_rus = 'Папка не подходит. Она либо не существует, либо это файл.'
            ms_receiver(m_rus)
            return
        if not Glue(path).init_happened():
            m = 'not a valid project'
            m_rus = 'Папка не подходит. Не удается открыть проект. Возможно в папке просто нет нужных файлов. Возможно что то не так с файлом конфигурации (config.json)'
            ms_receiver(m_rus)
            return
        m = 'project found'
        m_rus = 'Все ок. Проект найден'
        ms_receiver(m_rus)
        return True

    def _open_and_proceed(self, user_input_path: str):
        path = Path(user_input_path)
        self.Path_Chosen.emit(path)
    pass
