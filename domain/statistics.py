from pathlib import Path
from domain.glue import Glue
from domain.submodules.copy_folder_manager import CopyFolderManager
from domain.submodules.lib_scanner import LibScanner
from domain.book_data_holders.description_stage import DescriptionStage


class Statistics:
    """container for numbers describing project state"""
    def __init__(self,
                 project_path: Path,
                 books_in_source_count,
                 preprocessed_books_count,
                 rejected_books_count,
                 finished_books_count,
                 not_started_books_count,
                 in_progress_books_count,
                 copied_books_without_source_count):
        self.project_path = project_path
        self.books_in_source_count = books_in_source_count
        self.preprocessed_books_count = preprocessed_books_count
        self.left_to_preprocess_books_count = books_in_source_count - preprocessed_books_count
        self.rejected_books_count = rejected_books_count
        self.finished_books_count = finished_books_count
        self.not_started_books_count = not_started_books_count
        self.in_progress_books_count = in_progress_books_count
        self.copied_books_without_source_count = copied_books_without_source_count
        pass

    @classmethod
    def make_statistics_from_project_path(cls, project_path: Path):
        # fixme: why so much code?
        manager = Glue(project_path).get_project_manager()

        config = manager.config
        source_books_paths = LibScanner.find_all_files(
            extensions=config.extensions,
            lib_root_path=manager.lib_root_path
        )

        source_books_paths_set = set(source_books_paths)

        all_preprocessed_book_folder_managers \
            = CopyFolderManager(manager.copy_folder_path)\
            .load_book_folders_managers()

        preprocessed_bfm_with_source = [bfm for bfm in all_preprocessed_book_folder_managers
                                        if Path(manager.project_folder, bfm.book_state.original_rel_path) in source_books_paths_set]

        rejected_bfm = [bfm for bfm in preprocessed_bfm_with_source if bfm.book_state.descr_stage == DescriptionStage.REJECTED]
        finished_bfm = [bfm for bfm in preprocessed_bfm_with_source if bfm.book_state.descr_stage == DescriptionStage.FINISHED]
        not_started_bfm = [bfm for bfm in preprocessed_bfm_with_source if bfm.book_state.descr_stage == DescriptionStage.NOT_STARTED]
        in_progress_bfm = [bfm for bfm in preprocessed_bfm_with_source if bfm.book_state.descr_stage == DescriptionStage.IN_PROGRESS]

        preprocessed_bfm_without_source = [bfm for bfm in all_preprocessed_book_folder_managers
                                           if Path(manager.project_folder, bfm.book_state.original_rel_path) not in source_books_paths_set]

        return Statistics(
            project_path,
            len(source_books_paths),
            len(preprocessed_bfm_with_source),
            len(rejected_bfm),
            len(finished_bfm),
            len(not_started_bfm),
            len(in_progress_bfm),
            len(preprocessed_bfm_without_source)
        )
