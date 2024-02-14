from pathlib import Path
from domain.book_data_holders.book_meta import BookMeta
from domain.book_data_holders.description_stage import DescriptionStage
from domain.book_data_holders.book_info import BookInfo
from collections import namedtuple

from domain.submodules.project_folder_manager import ProjectFolderManager
from domain.book_data_holders.book_folder_manager import BookFolderManager

FullListRecord = namedtuple('FullListRecord', 'rel_path descr_stage')


class Engine:
    def __init__(self, project_folder_manager: ProjectFolderManager,
                 book_folder_managers: list):
        self.project_folder_manager = project_folder_manager
        self.config = self.project_folder_manager.config
        self.meta_scheme = self.config.get_meta_scheme()
        self.book_folder_managers = book_folder_managers
        self._current_book_index = 0
        pass

    def save_book_data(self, book_meta: BookMeta, stage: DescriptionStage, message: str = None):
        """save progress with this"""
        if stage == DescriptionStage.NOT_STARTED:
            raise ValueError(f'current stage must not be {DescriptionStage.NOT_STARTED} == not started')

        folder_manager = self._get_current_book_folder_manager()
        folder_manager: BookFolderManager
        folder_manager.save_book_meta(book_meta)

        folder_manager.book_state.descr_stage = stage
        if message is not None:
            folder_manager.book_state.message = message
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

    # def set_message_to_current_book(self, message: str):
    #     book_folder_manager = self._get_current_book_folder_manager()
    #     book_folder_manager: BookFolderManager
    #     book_folder_manager.book_state.message = message
    #     pass

    def get_full_book_list(self):
        """indexes are the same (with what they are the same???!)
        guess that you should look up a book from this list and then select
        it via try_set_book_index
        DO NOT use rel_path in any way except for showing book name. pls"""
        # todo: these records are low informative
        # todo: check that it is ok to give it abs_path in higher versions
        return [FullListRecord(rel_path=Path(fm.meta.initial_file_name),
                               descr_stage=fm.book_state.descr_stage)
                for fm in self.book_folder_managers]

    @property
    def current_book_index(self):
        return self._current_book_index

    def try_set_book_index(self, index: int):
        if -1 < index < len(self.book_folder_managers):
            self._current_book_index = index
            return True
        return False

    def _get_current_book_folder_manager(self):
        return self.book_folder_managers[self._current_book_index]
    pass
