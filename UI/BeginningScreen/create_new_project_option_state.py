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
        m1 = 'please select folder in which project files will be stored'
        m1_rus = 'Пожалуйста, выберите папку, в которой будут созданы файлы проекта'
        self.main_widget = PathChoosingWidget(
            input_description=m1_rus,
            return_button_text='Назад',
            input_field_hint='Вводить путь здесь (можно еще выбрать в проводнике кнопкой справа)',
            continue_button_text='Продолжить',
            default_feedback='Здесь будет написано, подходит выбранная папка или нет',
        )
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
            m = 'path must be absolute'
            m_rus = 'Папка не подходит. Путь должен быть абсолютным (начинаться с буквы диска. Например E:/...'
            ms_receiver(m_rus)
            return
        if path.is_file():
            m = 'path must represent a folder, not a file'
            m_rus = 'Папка не подходит. Это же не папка, а файл.'
            ms_receiver(m_rus)
            return
        m = f'project files will be located at {path}'
        m_rus = f'Все ок. Файлы проекта будут расположены в {path}'
        ms_receiver(m_rus)
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
