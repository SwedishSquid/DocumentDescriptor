from pathlib import Path
from domain.new.workstate_handler.work_state import WorkState
from domain.new.book_data_holders.book_record import BookRecord
from domain.new.book_data_holders.book_meta import BookMeta
from domain.new.meta_handler.meta_filehandler import MetaFilehandler
from domain.new.book_data_holders.description_stage import DescriptionStage
from domain.new.config_handler.my_config_reader import MyConfigReader
from domain.new.book_data_holders.readme_handler.readme_reader import ReadmeReader


class Engine:
    config_file_name = 'config.json'
    lib_dir_name = 'lib_root'
    workstate_file_name = 'workstate.json'
    readme_file_name = 'README'

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

        self.readme_reader = ReadmeReader(self.config_reader.get_book_meta_scheme())
        pass

    def _get_book_record(self, index: int):
        result = None
        if -1 < index < len(self.workstate.book_records):
            result: BookRecord = self.workstate.book_records[index]
            self._current_book_index = index
        return result

    def _get_next_book_record(self):
        return self._get_book_record(self._current_book_index + 1)

    def _get_book_meta(self, index: int):
        book_record = self._get_book_record(index)
        if book_record is None:
            return None

        result_meta: BookMeta

        if book_record.description_stage == DescriptionStage.NOT_STARTED:
            abs_old_book_path = Path(self.lib_root_path,  book_record.old_book_path)
            abs_old_dir_path = abs_old_book_path.parent
            abs_readme_path = Path(abs_old_dir_path, self.readme_file_name)
            if abs_readme_path.exists() and abs_readme_path.is_file():
                result_meta = self.readme_reader.read(abs_readme_path)
            else:
                result_meta = self.config_reader.get_book_meta_scheme().make_empty_book_meta()
            self.save_book_data(result_meta, DescriptionStage.IN_PROGRESS)
        else:
            abs_new_book_path = Path(self.lib_root_path, book_record.new_book_path)
            abs_new_dir_path = abs_new_book_path.parent
            result_meta = self.meta_filehandler.read_from_file(abs_new_dir_path)
        return result_meta

    def save_book_data(self, book_meta: BookMeta, current_stage: DescriptionStage):
        if current_stage == DescriptionStage.NOT_STARTED:
            raise ValueError(f'current stage must not be {DescriptionStage.NOT_STARTED} == not started')
        book_record: BookRecord = self.workstate.book_records[self._current_book_index]
        prev_stage = book_record.description_stage
        if prev_stage == DescriptionStage.NOT_STARTED:
            book_record = self._move_book_file(book_record)
        book_record.description_stage = current_stage
        self.workstate.book_records[self._current_book_index] = book_record
        self.workstate.dump_to_file(self.workstate_path)

        abs_book_dir_path = Path(self.lib_root_path, book_record.new_book_path.parent)
        self.meta_filehandler.write_book_meta(book_meta, abs_book_dir_path)
        pass

    def get_current_book(self):
        meta = self._get_book_meta(self._current_book_index)
        rel_path = self._get_book_record(self._current_book_index).new_book_path
        path = Path(self.lib_root_path, rel_path)
        return path, meta

    @property
    def current_book_index(self):
        return self._current_book_index

    def try_set_book_index(self, index: int):
        if -1 < index < len(self.workstate.book_records):
            self._current_book_index = index
            return True
        return False

    def _move_book_file(self, book_record: BookRecord):
        relative_dir_path = book_record.old_book_path.with_suffix('')
        abs_dir_path = Path(self.lib_root_path, relative_dir_path)
        if not abs_dir_path.exists():
            abs_dir_path.mkdir()
        rel_new_book_path = Path(relative_dir_path, book_record.old_book_path.name)
        book_record.new_book_path = rel_new_book_path
        # move
        abs_new_book_path = Path(self.lib_root_path, rel_new_book_path)
        abs_old_book_path = Path(self.lib_root_path, book_record.old_book_path)
        abs_old_book_path.rename(abs_new_book_path)
        book_record.description_stage = DescriptionStage.IN_PROGRESS
        return book_record

    def _scan_lib(self):
        '''get relative paths from lib_root to every file of book-like extension'''
        patterns = ['*.djvu', '*.pdf']
        absolute_paths = []
        for pattern in patterns:
            for p in self.lib_root_path.rglob(pattern):
                if p.is_file():
                    absolute_paths.append(p)
        relative_paths = [Path(*p.parts[len(self.lib_root_path.parts):]) for p in
                          absolute_paths]
        return relative_paths
    pass
