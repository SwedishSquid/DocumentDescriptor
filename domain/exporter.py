from domain.submodules.project_folder_manager import ProjectFolderManager
from domain.submodules.lib_scanner import LibScanner
from domain.submodules.copy_folder_manager import CopyFolderManager
from domain.book_data_holders.description_stage import DescriptionStage
from domain.book_data_holders.book_folder_manager import BookFolderManager
import utils
from pathlib import Path
import logging


class Exporter:
    """supposed to help a bit to export described books"""
    _finished_export_folder_name = 'finished'
    _rejected_export_folder_name = 'rejected'

    def __init__(self, project_folder_manager: ProjectFolderManager):
        self.manager = project_folder_manager
        self.logger = logging.getLogger(__name__)
        pass

    @property
    def finished_export_folder(self):
        return Path(self.manager.export_folder_path, self._finished_export_folder_name)

    @property
    def rejected_export_folder(self):
        return Path(self.manager.export_folder_path, self._rejected_export_folder_name)

    def export_finished_books(self):
        """considers IN_PROGRESS to be finished too"""
        self.logger.info('exporting finished books')
        self._export_whatever(
            export_to=self.finished_export_folder,
            acceptable_descr_stages=[DescriptionStage.FINISHED,
                                     DescriptionStage.IN_PROGRESS])
        pass

    def export_rejected_books(self):
        self.logger.info('exporting rejected books')
        self._export_whatever(export_to=self.rejected_export_folder,
                              acceptable_descr_stages=[DescriptionStage.REJECTED],
                              do_export_book_state=True)
        pass

    def get_all_sourced_bfm(self):
        """bfm == book folder manager;
        sourced == original book can be found"""
        source_books_paths = set(LibScanner.find_all_files(
            extensions=self.manager.config.extensions,
            lib_root_path=self.manager.lib_root_path
        ))
        # bfm == book folder manager
        all_preprocessed_bfm_in_copy_folder \
            = CopyFolderManager(self.manager.copy_folder_path) \
            .load_book_folders_managers()
        sourced_bfm = [bfm for bfm in all_preprocessed_bfm_in_copy_folder
                       if self.manager.make_absolute_path(bfm.original_relative_filepath) in source_books_paths]
        self.logger.debug(f'found {len(sourced_bfm)} sourced books in copy folder')
        return sourced_bfm

    def get_sourced_bfm_by_descr_stage(self, acceptable_descr_stages: list):
        # bfm == book folder manager
        return [bfm for bfm in self.get_all_sourced_bfm()
                if bfm.book_state.descr_stage in acceptable_descr_stages]

    def _export_whatever(self, export_to: Path, acceptable_descr_stages: list,
                         do_export_book_state=False):
        """:param export_to: folder where to put files as export result"""
        # bfm == book folder manager
        bfm_to_export = self.get_sourced_bfm_by_descr_stage(
            acceptable_descr_stages
        )
        self.logger.debug(f'found {len(bfm_to_export)} books to export')
        for bfm in bfm_to_export:
            export_book_subfolder = Path(export_to, bfm.folder_path.name)
            utils.make_directory(export_book_subfolder, parents=True, exist_ok=True)
            self._copy_meta_file(bfm, export_book_subfolder)
            self._copy_original_book(bfm, export_book_subfolder)
            if do_export_book_state:
                self._copy_bookstate_file(bfm, export_book_subfolder)
        pass

    def _copy_meta_file(self, bfm: BookFolderManager, export_book_subfolder: Path):
        new_filepath = Path(export_book_subfolder, bfm.meta_filepath.name)
        utils.copy_file(bfm.meta_filepath,
                        new_filepath)
        pass

    def _copy_bookstate_file(self, bfm: BookFolderManager, export_book_subfolder):
        new_filepath = Path(export_book_subfolder, bfm.book_state_filepath.name)
        utils.copy_file(bfm.book_state_filepath,
                        new_filepath)
        pass

    def _copy_original_book(self, bfm: BookFolderManager, export_book_subfolder: Path, new_file_stem='book'):
        """:param new_file_stem: stem == filename without extension"""
        source_book_path = self.manager.make_absolute_path(
            bfm.original_relative_filepath
        )
        new_bookfile_name = source_book_path.with_stem(new_file_stem).name
        new_filepath = Path(export_book_subfolder, new_bookfile_name)
        utils.copy_file(source_book_path,
                        new_filepath)
        pass
    pass
