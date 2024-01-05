from pathlib import Path

import ocrmypdf

from domain.submodules.state import State
from domain.submodules.lib_scanner import LibScanner

from domain.book_data_holders.book_folder_manager import BookFolderManager
from domain.converters import djvu_to_pdf
from domain.submodules.project_folder_manager import ProjectFolderManager
import utils


class Preprocessor:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.proj_folder_manager = ProjectFolderManager(project_dir)
        self.config = self.proj_folder_manager.config
        self.do_book_recognition = False
        pass

    def preprocess_with_generator(self):
        """yields current preprocessed count and total amount"""
        # todo: check if already preprocessed
        if State.exists(self.project_dir):
            raise FileExistsError('it seems that preprocessing already took place')

        books_abs_paths = LibScanner.find_all_files(self.config.extensions,
                                                    lib_root_path=self.proj_folder_manager.lib_root_path)

        books_to_preprocess_paths = books_abs_paths

        count = 0
        total_amount = len(books_to_preprocess_paths)

        yield count, total_amount

        for p in books_to_preprocess_paths:
            self.preprocess_book(p)
            count += 1
            yield count, total_amount

        folders_paths = [p.with_suffix('') for p in books_abs_paths]

        State.create_new(self.project_dir, folders_paths)
        pass

    def preprocess_book(self, book_path: Path):
        folder_manager = BookFolderManager.create_folder_from(book_path, self.config)
        self._populate_temp_folder_with_pdf(folder_manager)
        pass

    def _populate_temp_folder_with_pdf(self, folder_manager: BookFolderManager):
        """
        makes showing copy of book in /temp if it is pdf; else converts and does the same;

        showing - means the one, that will be put in pdf_view widget
        """
        original = folder_manager.original_book_path
        extension = original.suffix.strip('.')
        if extension == 'pdf':
            self._make_book_for_showing(original, folder_manager.temp_book_path)
        elif extension == 'djvu':
            djvu_to_pdf.convert_djvu_to_pdf(original, folder_manager.temp_book_path)
            self._make_book_for_showing(folder_manager.temp_book_path)
        else:
            raise ValueError(f'book files with {extension} extension not supported; got on file {original}')
        pass

    # todo: somehow specify language of the book
    def _make_book_for_showing(self, source, destination=None):
        if self.do_book_recognition:
            Preprocessor._make_recognized_copy(source, destination)
        else:
            utils.copy_file(source, destination)

    @staticmethod
    def _make_recognized_copy(source, destination=None, language="rus"):
        """replaces source pdf if destination not stated,

        Parameters
        ----------
        language: [str] | str
            possible values: "eng", "rus", ...
            works fine only with single language
        """
        if destination is None:
            destination = source
        try:
            ocrmypdf.ocr(source, destination, language=language)
        except ocrmypdf.exceptions.PriorOcrFoundError:
            # in case text already exists
            utils.copy_file(source, destination)
        except ocrmypdf.exceptions.MissingDependencyError:
            print("Some dependency missing")
            raise
        except Exception as e:
            raise
