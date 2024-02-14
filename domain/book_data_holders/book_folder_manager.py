from pathlib import Path

from domain.book_state import BookState
from domain.submodules.meta_filehandler import MetaFilehandler
from domain.book_data_holders.book_meta import BookMeta
from domain.book_data_holders.description_stage import DescriptionStage
from domain.book_data_holders.book_meta_scheme import BookMetaScheme
from domain.submodules.readme_reader import ReadmeReader
import re
import utils


class BookFolderManager:
    _copy_filename = 'copy.pdf'
    _book_state_file_name = 'book_state.json'
    _unique_folder_index = 0
    _book_folder_name_common_prefix = 'book'

    def __init__(self, sequence_number: int, book_folder_path: Path, meta: BookMeta, book_state: BookState):
        self.sequence_number = sequence_number
        self.folder_path = Path(book_folder_path)
        if not self.folder_path.is_absolute():
            raise ValueError(f'book_folder_path must be absolute; got {book_folder_path}')

        self.book_state_filepath = Path(book_folder_path,
                                        self._book_state_file_name)

        self.book_state = book_state

        self.meta = meta

        self._book_copy_path = Path(self.folder_path,
                                    self._copy_filename)
        pass

    @property
    def temp_book_path(self):
        return self._book_copy_path

    @property
    def meta_filepath(self):
        return Path(self.folder_path, MetaFilehandler.filename)

    @property
    def original_relative_filepath(self):
        """returns original filepath relative to project root"""
        return self.book_state.original_rel_path

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
        return BookState.loads(utils.read_text_from_file(self.book_state_filepath))

    def _dump_book_state(self):
        utils.write_text_to_file(self.book_state_filepath,
                                 self.book_state.dumps())
        pass

    def _load_meta_data(self):
        return MetaFilehandler().read_from_file(self.folder_path)

    def _dump_my_meta_data(self):
        return self._dump_meta_data(self.meta, self.folder_path)

    @classmethod
    def _dump_meta_data(cls, meta: BookMeta, folder_path):
        return MetaFilehandler().write_book_meta(meta, path_to_book_dir=folder_path)

    @classmethod
    def load_from_path(cls, folder: Path, ms_receiver=None):
        """returns None if cannot read"""
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)
        # todo: log unexpected things
        try:
            state_path = Path(folder, cls._book_state_file_name)
            book_state = BookState.loads(utils.read_text_from_file(state_path))
            meta = MetaFilehandler().read_from_file(folder)
            sequence_number = cls._get_sequence_number_from_folder_path(folder)
        except Exception as e:
            ms_receiver(str(e))
            return None
        return BookFolderManager(sequence_number=sequence_number,
                                 book_folder_path=folder,
                                 meta=meta,
                                 book_state=book_state)

    @classmethod
    def write_new_folder(cls, book_file: Path, where_to_place_folder: Path,
                         meta_scheme: BookMetaScheme, original_book_rel_path: Path):
        folder = cls._get_available_book_folder_path(where_to_place_folder)
        utils.make_directory(folder, parents=True)
        sequence_number = cls._get_sequence_number_from_folder_path(folder)

        meta = cls._create_meta(book_folder=book_file.parent, meta_scheme=meta_scheme,
                                initial_filename=book_file.name)
        # todo: log readme reading maybe
        cls._dump_meta_data(meta, folder)       # meta

        state = BookState(original_rel_path=original_book_rel_path, descr_stage=DescriptionStage.NOT_STARTED, preprocessed=False)
        state_filepath = Path(folder, cls._book_state_file_name)
        utils.write_text_to_file(state_filepath, state.dumps())         # state
        return BookFolderManager(sequence_number=sequence_number,
                                 book_folder_path=folder,
                                 meta=meta, book_state=state)

    @classmethod
    def _get_sequence_number_from_folder_path(cls, folder_path: Path):
        s = folder_path.name
        pattern = rf'{cls._book_folder_name_common_prefix}(\d+)'
        match = re.match(pattern, s)
        num = int(match.groups()[0])
        return num

    @classmethod
    def _get_available_book_folder_path(cls, parent_folder: Path):
        while True:
            book_folder_name = cls._book_folder_name_common_prefix + str(cls._get_unique_folder_index())
            folder = Path(parent_folder, book_folder_name)
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
    def _create_meta(cls, book_folder, meta_scheme: BookMetaScheme, initial_filename: str):
        # todo: maybe add option to delete README afterwards
        readme_path = cls._find_readme(book_folder)
        scheme = meta_scheme
        if readme_path is None:
            meta = scheme.make_empty_book_meta()
        else:
            meta = ReadmeReader(scheme).read(readme_path)
        meta.initial_file_name = initial_filename
        return meta
    pass
