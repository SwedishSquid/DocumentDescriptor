from pathlib import Path
from domain.submodules.project_folder_manager import ProjectFolderManager
from domain.preprocessor import Preprocessor
from domain.submodules.copy_folder_manager import CopyFolderManager
from domain.submodules.lib_scanner import LibScanner
from domain.book_data_holders.book_folder_manager import BookFolderManager
from domain.engine import Engine
from domain.exporter import Exporter


class Glue:
    """some strange module
     made in attempt to unite descriptor and preprocessor
     and exporter"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        pass

    def init_happened(self, ms_receiver=None):
        proj_manager = self.get_project_manager(ms_receiver)
        return proj_manager is not None

    def get_project_manager(self, ms_receiver=None):
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)
        return ProjectFolderManager.load_from_path(self.project_path,
                                                   ms_receiver=ms_receiver)

    def init_project(self, ms_receiver=None):
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)
        ProjectFolderManager.init_project(self.project_path, ms_receiver=ms_receiver)
        pass

    def get_preprocessor_generator(self, ms_receiver=None):
        """:returns: generator_object and books_count"""
        # todo: remove ms_receiver
        project_manager = self.get_project_manager(ms_receiver)
        if not project_manager:
            raise FileNotFoundError('check before calling this method')

        config = project_manager.config

        copy_folder_manager = CopyFolderManager(
            project_manager.copy_folder_path)
        copy_folder_manager.delete_all_not_preprocessed_bfm()

        already_preprocessed_bfm = copy_folder_manager.load_book_folders_managers()

        original_books = LibScanner.find_all_files(config.extensions,
                                                   project_manager.lib_root_path)

        books_to_preprocess = self._get_not_preprocessed_books(
            all_original_books=original_books,
            already_preprocessed_bfm=already_preprocessed_bfm)

        books_count = len(books_to_preprocess)
        generator = Preprocessor(project_manager).preprocess_with_generator(books_to_preprocess)
        return generator, books_count

    def get_engine(self, ms_receiver=None):
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)
        if not self.init_happened():
            raise ValueError('cant get engine - project not valid; run preprocessor init first')
        proj_manager = self.get_project_manager()

        copy_folder_manager = CopyFolderManager(
            proj_manager.copy_folder_path)
        copy_folder_manager.delete_all_not_preprocessed_bfm()

        already_preprocessed_bfm = copy_folder_manager.load_book_folders_managers()

        return Engine(project_folder_manager=proj_manager, book_folder_managers=already_preprocessed_bfm)

    def get_exporter(self):
        return Exporter(self.get_project_manager())

    def is_preprocessed(self, ms_receiver=None):
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)
        project_manager = self.get_project_manager(ms_receiver)
        if not project_manager:
            raise FileNotFoundError('check before calling this method')

        config = project_manager.config

        copy_folder_manager = CopyFolderManager(
            project_manager.copy_folder_path)
        copy_folder_manager.delete_all_not_preprocessed_bfm()
        original_books = LibScanner.find_all_files(config.extensions,
                                                   project_manager.lib_root_path)
        already_preprocessed_bfm = copy_folder_manager.load_book_folders_managers()

        books_to_preprocess = self._get_not_preprocessed_books(
            all_original_books=original_books,
            already_preprocessed_bfm=already_preprocessed_bfm)
        return len(books_to_preprocess) == 0

    def _get_not_preprocessed_books(self, all_original_books: list,
                                    already_preprocessed_bfm: list):
        project_manager = self.get_project_manager()
        finished_rel = set()

        result = []
        for bfm in already_preprocessed_bfm:
            bfm: BookFolderManager = bfm
            finished_rel.add(bfm.original_relative_filepath)
        for book in all_original_books:
            book: Path = book
            rel_p = project_manager.make_relative_path(book)
            if rel_p in finished_rel:
                continue
            result.append(book)
        return result
