from pathlib import Path

import utils
from domain.submodules.config import Config, FieldConfigRecord, OCRConfig


class ProjectConsistencyError(Exception):
    """raised when some parts of the project missing or not consistent"""


class ProjectFolderManager:
    _config_file_name = 'config.json'

    def __init__(self, project_folder):
        self.project_folder = Path(project_folder)
        self.check_project_consistency(project_folder)

        self.config_path = Path(self.project_folder, self._config_file_name)
        self.config = Config.loads(utils.read_text_from_file(self.config_path))
        pass

    @property
    def lib_root_path(self):
        return Path(self.project_folder, self.config.lib_root_folder_name)

    @classmethod
    def _probe_project_folder(cls, project_folder: Path, raise_exc=False):
        ans = project_folder.is_dir()
        if not ans and raise_exc:
            raise NotADirectoryError(f'project folder must be a directory and exist; got {project_folder}')
        return ans

    @classmethod
    def check_project_consistency(cls, project_folder: Path):
        cls._probe_project_folder(project_folder, True)
        cls.probe_config_file(project_folder, True)
        cls._probe_lib_root(project_folder, True)
        pass

    @classmethod
    def init_project(cls, project_folder: Path):
        cls._probe_project_folder(project_folder, raise_exc=True)
        result_message = []
        if not cls.probe_config_file(project_folder):
            cls.create_default_config_file(project_folder)
            result_message.append('default config created')
        else:
            result_message.append('config already exists')
        if not cls._probe_lib_root(project_folder):
            config = Config.loads(utils.read_text_from_file(
                Path(project_folder, cls._config_file_name)))
            lib_root_path = Path(project_folder, config.lib_root_folder_name)
            utils.make_directory(lib_root_path)
            result_message.append('empty lib root folder created')
        else:
            result_message.append('lib root folder already exists')
        return result_message

    @classmethod
    def _probe_lib_root(cls, project_folder: Path, raise_exc=False):
        config = Config.loads(utils.read_text_from_file(
            Path(project_folder, cls._config_file_name)))
        lib_root_path = Path(project_folder, config.lib_root_folder_name)
        ans = lib_root_path.is_dir()
        if not ans and raise_exc:
            raise NotADirectoryError(f'lib root directory (named {config.lib_root_folder_name}) not found')
        return ans

    @classmethod
    def probe_config_file(cls, project_folder: Path, raise_exc=False):
        cls._probe_project_folder(project_folder, raise_exc=True)
        config_path = Path(project_folder, cls._config_file_name)
        ans = config_path.is_file()
        if not ans and raise_exc:
            raise FileNotFoundError(f'config file not found at {config_path}')
        return ans

    @classmethod
    def create_default_config_file(cls, project_folder: Path):
        cls._probe_project_folder(project_folder)
        ocr_config = OCRConfig(pages_arg='1-5', language_arg='rus+eng', do_ocr=True)
        conf = Config(
            [FieldConfigRecord('author', 'Автор', 'Author'),
             FieldConfigRecord('title', 'Название', 'Title'),
             FieldConfigRecord('publisher', 'Издатель', 'Publisher'),
             FieldConfigRecord('pages', 'Количество страниц', 'Pages'),
             FieldConfigRecord('year', 'Год издания', 'Year'),
             FieldConfigRecord('field_with_no_readme_field', 'Поле без соответствующего поля в README', None)],
            ['.pdf', '.djvu'], lib_root_folder_name='lib_root',
            orc_config=ocr_config)
        utils.write_text_to_file(Path(project_folder, cls._config_file_name),
                                 text=conf.dumps())
        return conf
    pass
