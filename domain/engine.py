from pathlib import Path
from domain.book_data_holders.book_meta import BookMeta
from domain.book_data_holders.description_stage import DescriptionStage
from domain.book_data_holders.book_info import BookInfo
from collections import namedtuple

from domain.submodules.project_folder_manager import ProjectFolderManager
from domain.submodules.state import State

FullListRecord = namedtuple('FullListRecord', 'rel_path descr_stage')


class Engine:
    def __init__(self, project_directory):
        """ожидаю, что конфиг существует + предобработка выполнена"""
        self.project_path = Path(project_directory)
        if not self.project_path.is_dir():
            raise NotADirectoryError(f'{self.project_path} is not a directory')

        if not State.exists(self.project_path):
            raise ValueError(f'state does not exist yet; preprocess before description')

        self.project_folder_manager = ProjectFolderManager(self.project_path)
        self.config = self.project_folder_manager.config
        self.meta_scheme = self.config.get_meta_scheme()
        self.proj_state = State(self.project_path)     # resource intensive operation

        self._current_book_index = 0
        self.try_set_book_index(self.proj_state.index)
        pass

    def save_book_data(self, book_meta: BookMeta, stage: DescriptionStage):
        """save progress with this"""
        if stage == DescriptionStage.NOT_STARTED:
            raise ValueError(f'current stage must not be {DescriptionStage.NOT_STARTED} == not started')

        folder_manager = self._get_current_book_folder_manager()
        folder_manager.save_book_meta(book_meta)

        folder_manager.book_state.descr_stage = stage
        folder_manager.save_book_state()
        pass

    def get_current_book(self):
        """return currently chosen book's info"""
        folder_manager = self._get_current_book_folder_manager()
        meta = folder_manager.meta
        info = BookInfo(
            book_meta=meta,
            absolute_path=folder_manager.temp_book_path,
            meta_scheme=self.meta_scheme,
            descr_stage=folder_manager.book_state.descr_stage
        )
        return info

    def get_full_book_list(self):
        """indexes are the same (with what they are the same???!)
        guess that you should look up a book from this list and then select
        it via try_set_book_index
        DO NOT use rel_path in any way except for showing book name. pls"""
        # todo: these records are low informative
        # todo: check that it is ok to give it abs_path in higher versions
        return [FullListRecord(rel_path=fm.folder_path,
                               descr_stage=fm.book_state.descr_stage)
                for fm in self.proj_state.book_folders_managers]

    @property
    def current_book_index(self):
        return self._current_book_index

    def try_set_book_index(self, index: int):
        if -1 < index < len(self.proj_state.book_folders):
            self._current_book_index = index
            self.proj_state.save_index(self._current_book_index)
            return True
        return False

    def _get_current_book_folder_manager(self):
        return self.proj_state.book_folders_managers[self._current_book_index]
    pass
