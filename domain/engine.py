from pathlib import Path
from domain.submodules.workstate.work_state import WorkState
from domain.submodules.workstate.workstate_book_record import WorkstateBookRecord
from domain.book_data_holders.book_meta import BookMeta
from domain.submodules.meta_filehandler import MetaFilehandler
from domain.book_data_holders.description_stage import DescriptionStage
from domain.submodules.my_config_reader import MyConfigReader
from domain.submodules.readme_reader import ReadmeReader
from domain.book_data_holders.book_info import BookInfo
from submodules.lib_scanner import LibScanner
from submodules.book_preprocessor import BookPreprocessor
from collections import namedtuple

FullListRecord = namedtuple('FullListRecord', 'rel_path descr_stage')


class Engine:
    config_file_name = 'config.json'
    lib_dir_name = 'lib_root'
    workstate_file_name = 'workstate.json'

    def __init__(self, project_directory, lib_dir_name=None):
        self.project_directory = Path(project_directory)
        if not self.project_directory.is_dir():
            raise NotADirectoryError(f'{self.project_directory} is not a directory')
        if lib_dir_name is not None:
            self.lib_dir_name = lib_dir_name

        self.config_path = Path(self.project_directory, self.config_file_name)
        if not self.config_path.exists():
            raise FileNotFoundError(f'{self.config_path} config file not found')

        self.config_reader = MyConfigReader(self.config_path)
        self.meta_scheme = self.config_reader.get_book_meta_scheme()

        self.lib_root_path = Path(self.project_directory, self.lib_dir_name)
        if not self.lib_root_path.exists():
            raise FileNotFoundError(f'{self.lib_root_path} not found')
        if not self.lib_root_path.is_dir():
            raise NotADirectoryError(f'{self.lib_root_path} is not a directory')

        self.workstate_path = Path(self.project_directory, self.workstate_file_name)
        if not self.workstate_path.exists():
            self.workstate = WorkState([])
        else:
            self.workstate = WorkState.load_from_file(self.workstate_path)

        self.workstate.update_with_paths(self._scan_lib())

        self._current_book_index = 0

        self.meta_filehandler = MetaFilehandler()

        readme_reader = ReadmeReader(self.meta_scheme)
        self.book_preprocessor = BookPreprocessor(self.lib_root_path,
                                                  readme_reader,
                                                  self.meta_scheme)
        pass

    def save_book_data(self, book_meta: BookMeta, stage: DescriptionStage):
        """save progress with this"""
        if stage == DescriptionStage.NOT_STARTED:
            raise ValueError(f'current stage must not be {DescriptionStage.NOT_STARTED} == not started')
        book_record = self._get_current_book_workstate_record()
        book_record.description_stage = stage
        self.workstate.dump_to_file(self.workstate_path)

        abs_book_dir_path = Path(self.lib_root_path, book_record.book_path.parent)
        self.meta_filehandler.write_book_meta(book_meta, abs_book_dir_path)
        pass

    def get_current_book(self):
        """return currently chosen book's info"""
        meta = self._get_book_meta()
        workstate_record = self._get_current_book_workstate_record()
        rel_path = workstate_record.book_path
        path = Path(self.lib_root_path, rel_path)
        info = BookInfo(meta, path, self.meta_scheme, workstate_record)
        return info

    def get_full_book_list(self):
        """indexes are the same"""
        return [FullListRecord(rel_path=record.book_path,
                               descr_stage=record.description_stage)
                for record in self.workstate.book_records]

    @property
    def current_book_index(self):
        return self._current_book_index

    def try_set_book_index(self, index: int):
        if -1 < index < len(self.workstate.book_records):
            self._current_book_index = index
            return True
        return False

    def _get_current_book_workstate_record(self) -> WorkstateBookRecord:
        return self.workstate.book_records[self._current_book_index]

    def _get_book_meta(self) -> BookMeta | None:
        """return book_meta for an index
        None if index not found"""
        workstate_record = self._get_current_book_workstate_record()
        if workstate_record is None:
            # - what does workstate_record == None even mean???
            # - it means that index is incorrect, me
            # - ah yeah, thanks
            return None

        if workstate_record.description_stage == DescriptionStage.NOT_STARTED:
            self._prepare_book()
            # replace old workstate_record in case it was changed
            workstate_record = self._get_current_book_workstate_record()

        abs_new_book_path = Path(self.lib_root_path, workstate_record.book_path)
        abs_new_dir_path = abs_new_book_path.parent
        result_meta = self.meta_filehandler.read_from_file(abs_new_dir_path)
        return result_meta

    def _prepare_book(self):
        """Только для ранее не открывавшихся книг.
         читает README, составляет BookMeta по нему или пустой,
          переносит книгу куда нужно, сохраняет BookMeta"""
        workstate_record = self._get_current_book_workstate_record()
        result_meta = self.book_preprocessor.preprocess(workstate_record)
        self.save_book_data(result_meta, DescriptionStage.IN_PROGRESS)
        pass

    def _scan_lib(self):
        """gets relative paths from lib_root to every file of book-like
        extension """
        extensions = ['djvu', 'pdf']

        scanner = LibScanner()
        absolute_paths = scanner.find_all_files(extensions, self.lib_root_path)

        relative_paths = [Path(*p.parts[len(self.lib_root_path.parts):]) for p in
                          absolute_paths]
        return relative_paths
    pass
