from pathlib import Path

from domain.book_state import BookState
from domain.submodules.meta_filehandler import MetaFilehandler
from domain.book_data_holders.book_meta import BookMeta
from domain.book_data_holders.description_stage import DescriptionStage
from domain.submodules.config import Config
from domain.submodules.readme_reader import ReadmeReader
import utils


class BookFolderManager:
    _temp_folder_name = 'temp'
    _book_copy_name = 'copy.pdf'
    _book_original_stem = 'original'            # filename without extension
    _book_state_file_name = 'book_state.json'
    _unique_folder_index = 0
    _book_folder_name_common_prefix = 'book'

    def __init__(self, book_folder_path):
        self.folder_path = Path(book_folder_path)
        if not self.folder_path.is_absolute():
            raise ValueError(f'book_folder_path must be absolute; got {book_folder_path}')

        self.book_state_filepath = Path(self.folder_path,
                                        self._temp_folder_name,
                                        self._book_state_file_name)
        self.book_state = self._load_book_state()

        self._original_book_path = Path(self.folder_path,
                                        self.book_state.name)

        self.meta = self._load_meta_data()

        self._book_copy_path = Path(self.folder_path,
                                    self._temp_folder_name,
                                    self._book_copy_name)
        pass

    @property
    def original_book_path(self):
        return self._original_book_path

    @property
    def temp_book_path(self):
        return self._book_copy_path

    def save_book_state(self, book_state: BookState = None):
        """if book_state == None, saves self.book_state"""
        if book_state is not None:
            self.book_state = book_state
        self._dump_book_state()
        pass

    def save_book_meta(self, meta: BookMeta = None):
        """if meta is None, saves self.meta"""
        if meta is not None:
            self.meta = meta
        self._dump_my_meta_data()
        pass

    def _load_book_state(self):
        return BookState.load_from_file(self.book_state_filepath)

    def _dump_book_state(self):
        self.book_state.dump_to_file(self.book_state_filepath)

    def _load_meta_data(self):
        return MetaFilehandler().read_from_file(self.folder_path)

    def _dump_my_meta_data(self):
        return self._dump_meta_data(self.meta, self.folder_path)

    @classmethod
    def _dump_meta_data(cls, meta: BookMeta, folder_path):
        return MetaFilehandler().write_book_meta(meta, path_to_book_dir=folder_path)

    @classmethod
    def create_folder_from(cls, book_file: Path, config: Config):
        cls._check_book_file(book_file)

        new_original_file_name = book_file.with_stem(cls._book_original_stem).name

        folder = cls._rearrange_book_files(book_file, new_original_file_name)

        cls._create_meta_file(folder, config, initial_filename=book_file.name)
        cls._create_book_state_file(folder, new_original_file_name)
        return BookFolderManager(folder)

    @classmethod
    def _get_available_book_folder_path(cls, book_file: Path):
        while True:
            book_folder_name = cls._book_folder_name_common_prefix + str(cls._get_unique_folder_index())
            folder = Path(book_file.parent, book_folder_name)
            if utils.exists(folder):
                continue
            return folder
        pass

    @classmethod
    def _get_unique_folder_index(cls):
        res = cls._unique_folder_index
        cls._unique_folder_index += 1
        return res

    @classmethod
    def _check_book_file(cls, book_file: Path):
        if not utils.exists(book_file):
            raise FileNotFoundError(f'cannot find {book_file}')
        if not utils.is_file(book_file):
            raise ValueError(f'{book_file} is not a file')
        pass

    @classmethod
    def _rearrange_book_files(cls, book_path: Path, new_original_file_name: str):
        """places book (named original.extension) and README file (if has one) into a new book folder
        creates temp folder
        :return: book folder path"""

        book_folder_path = cls._get_available_book_folder_path(book_path)

        utils.make_directory(book_folder_path)        # make result folder
        utils.make_directory(Path(book_folder_path, cls._temp_folder_name))   # make temp folder
        utils.move_file(book_path, Path(book_folder_path, new_original_file_name))
        readme_path = cls._find_readme(book_path.parent)
        if readme_path is not None:
            utils.move_file(readme_path, Path(book_folder_path, readme_path.name))
        return book_folder_path

    @classmethod
    def _find_readme(cls, dir_to_search):
        """returns None if no readme found"""
        # todo: get readme_name from config maybe??
        readme_name = 'README'
        readme_path = Path(dir_to_search, readme_name)
        if not readme_path.is_absolute():
            raise ValueError(
                f'dir_to_search must be absolute path; got {dir_to_search}')
        if utils.is_file(readme_path):
            return readme_path
        return None

    @classmethod
    def _create_meta_file(cls, book_folder, config: Config, initial_filename: str):
        # todo: maybe add option to delete README afterwards
        readme_path = cls._find_readme(book_folder)
        scheme = config.get_meta_scheme()
        if readme_path is None:
            meta = scheme.make_empty_book_meta()
        else:
            meta = ReadmeReader(scheme).read(readme_path)
        meta.initial_file_name = initial_filename
        cls._dump_meta_data(meta, book_folder)
        pass

    @classmethod
    def _create_book_state_file(cls, book_folder, book_name):
        BookState(book_name, DescriptionStage.NOT_STARTED) \
            .dump_to_file(Path(book_folder,
                               cls._temp_folder_name,
                               cls._book_state_file_name))
        pass


    pass
