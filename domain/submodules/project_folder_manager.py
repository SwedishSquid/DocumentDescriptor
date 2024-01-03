from pathlib import Path

import utils
from domain.submodules.config import Config, FieldConfigRecord


class ProjectFolderManager:
    _config_file_name = 'config.json'

    def __init__(self, project_folder):
        self.project_folder = Path(project_folder)
        self.check_project_folder(self.project_folder)

        self.config_path = Path(self.project_folder, self._config_file_name)
        if not self.config_path.exists():
            raise FileNotFoundError(f'config file not exists')
        self.config = self._load_config()
        pass

    @property
    def lib_root_path(self):
        return Path(self.project_folder, self.config.lib_root_folder_name)

    def _load_config(self):
        return Config.loads(utils.read_text_from_file(self.config_path))

    @classmethod
    def check_project_folder(cls, project_folder: Path):
        if not project_folder.is_dir():
            raise NotADirectoryError(f'project folder must be a directory and exist; got {project_folder}')
        pass

    @classmethod
    def probe_config_file(cls, project_folder: Path):
        cls.check_project_folder(project_folder)
        return Path(project_folder, cls._config_file_name).exists()

    @classmethod
    def create_default_config_file(cls, project_folder: Path):
        cls.check_project_folder(project_folder)
        conf = Config(
            [FieldConfigRecord('author', 'Автор', 'Author'),
             FieldConfigRecord('title', 'Название', 'Title'),
             FieldConfigRecord('publisher', 'Издатель', 'Publisher'),
             FieldConfigRecord('pages', 'Количество страниц', 'Pages'),
             FieldConfigRecord('year', 'Год издания', 'Year'),
             FieldConfigRecord('field_with_no_readme_field', 'Поле без соответствующего поля в README', None)],
            ['.pdf', '.djvu'], lib_root_folder_name='lib_root')
        utils.write_text_to_file(Path(project_folder, cls._config_file_name),
                                 conf._dumps())
        return conf

    pass
