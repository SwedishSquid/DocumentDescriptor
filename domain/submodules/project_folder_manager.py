from pathlib import Path
import logging
import utils
from domain.submodules.config import Config, ConfigFormatError


class ProjectFolderManager:
    _config_file_name = 'config.json'
    _copy_folder_name = 'copy'
    _export_folder_name = 'export'
    _ocr_output_filename = 'ocr_stdout.txt'
    _djvu_converter_output_filename = 'djvu_converter_stdout.txt'

    def __init__(self, project_folder, config: Config):
        self.project_folder = Path(project_folder)
        self.config = config
        pass

    @property
    def lib_root_path(self):
        return Path(self.project_folder, self.config.lib_root_folder_name)

    @property
    def export_folder_path(self):
        return Path(self.project_folder, self._export_folder_name)

    @property
    def copy_folder_path(self):
        return Path(self.project_folder, self._copy_folder_name)

    @property
    def stderr_ocr_filepath(self):
        return Path(self.project_folder, self._ocr_output_filename)

    @property
    def stderr_djvu_converter_filepath(self):
        return Path(self.project_folder, self._djvu_converter_output_filename)

    @classmethod
    def load_from_path(cls, project_path: Path, ms_receiver=None):
        """loads ProjectFolderManager from project folder
         returns None if not correct project
         :param ms_receiver: function that takes str - for logging purposes"""
        logger = logging.getLogger(__name__)
        logger.info('start loading project folder manager from path')
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)

        conf_path = Path(project_path, cls._config_file_name)
        config = cls._load_config(conf_path, ms_receiver)
        if config is None:
            logger.debug('config cant be loaded; stop loading project folder manager')
            return None

        copy_folder = Path(project_path, cls._copy_folder_name)
        if not utils.is_dir(copy_folder):
            logger.debug('no copy folder found; creating new')
            ms_receiver('has no copy folder; attempt to create')
            utils.make_directory(copy_folder)

        source_folder = Path(project_path, config.lib_root_folder_name)
        if not source_folder.is_dir():
            logger.debug(f'no source folder named {config.lib_root_folder_name} found; cant create project folder manager')
            ms_receiver(f'has no source folder; was looking for folder named {config.lib_root_folder_name}')
            return None
        logger.info('project folder manager loading finished')
        return ProjectFolderManager(project_folder=project_path, config=config)

    @classmethod
    def init_project(cls, project_path: Path, ms_receiver=None):
        """init or validate project"""
        logger = logging.getLogger(__name__)
        logger.info('project initiation started')
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)
        conf_path = Path(project_path, cls._config_file_name)
        if not utils.is_file(conf_path):
            logger.info('found no config file; creating new')
            cls.create_default_config_file(project_path)
            ms_receiver('add confing')
        else:
            logger.info('config file already exists')
            ms_receiver('config exists')

        copy_folder = Path(project_path, cls._copy_folder_name)
        if not utils.is_dir(copy_folder):
            logger.info('copy folder not found; creating new')
            ms_receiver('added copy folder')
            utils.make_directory(copy_folder)
        else:
            logger.info('copy folder exists')
            ms_receiver('copy folder exists')

        config = cls._load_config(conf_path, ms_receiver)
        if config is None:
            # todo: check if everything that uses this method check for None value
            logger.info('config folder cant be loaded; stop initiation')
            return
        source_folder = Path(project_path, config.lib_root_folder_name)
        if not utils.is_dir(source_folder):
            logger.info(f'no source folder found; creating new named {config.lib_root_folder_name}')
            utils.make_directory(source_folder)
            ms_receiver(f'added lib root folder named {config.lib_root_folder_name}')
        else:
            logger.info('lib root folder exists')
            ms_receiver('lib root folder exists')
    pass

    @classmethod
    def _load_config(cls, filepath: Path, ms_receiver):
        logger = logging.getLogger(__name__)
        if not filepath.is_file():
            ms_receiver('config not found')
            return None
        try:
            config = Config.loads(utils.read_text_from_file(filepath))
        except ConfigFormatError as e:
            logger.warning(f'config format error caught')
            logger.exception(e)
            ms_receiver(f'config format err: {e}')
            return None
        return config

    @classmethod
    def _probe_project_folder(cls, project_folder: Path, raise_exc=False):
        ans = project_folder.is_dir()
        if not ans and raise_exc:
            raise NotADirectoryError(f'project folder must be a directory and exist; got {project_folder}')
        return ans

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
        conf = Config.get_default()
        utils.write_text_to_file(Path(project_folder, cls._config_file_name),
                                 text=conf.dumps())
        return conf
    pass

    def make_relative_path(self, book_folder_path: Path):
        project_path = self.project_folder
        if not project_path.is_absolute():
            raise ValueError('project_path must be absolute')
        proj_path_parts_len = len(project_path.parts)
        if not Path(*book_folder_path.parts[:proj_path_parts_len]).match(
                str(project_path)):
            raise ValueError(
                f'book folders must be inside project folder; proj: {project_path}; book_folder: {book_folder_path}')
        return Path(*book_folder_path.parts[proj_path_parts_len:])

    def make_absolute_path(self, relative_to_project_folder_path: Path):
        return Path(self.project_folder, relative_to_project_folder_path)