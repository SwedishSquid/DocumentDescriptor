from pathlib import Path

from domain.external_parts.recognizer import Recognizer

from domain.book_data_holders.book_folder_manager import BookFolderManager
from domain.external_parts import djvu_to_pdf
from domain.submodules.project_folder_manager import ProjectFolderManager
import utils
import logging


class PreprocessError(Exception):
    """raise when can`t preprocess document"""


class Preprocessor:
    """Core of preprocessor part.
    Long automated tasks are made with this.
    Examples: copying files, converting them to pdf, applying OCR"""

    def __init__(self, project_folder_manager: ProjectFolderManager):
        self.proj_folder_manager = project_folder_manager
        self.project_dir = self.proj_folder_manager.project_folder
        self.config = self.proj_folder_manager.config
        self.logger = logging.getLogger(__name__)
        pass

    def preprocess_with_generator(self, original_books_to_preprocess: list):
        """yields current preprocessed count and total amount"""

        count = 0
        total_amount = len(original_books_to_preprocess)

        yield count, total_amount

        for abs_p in original_books_to_preprocess:
            rel_p = self.proj_folder_manager.make_relative_path(abs_p)
            bfm = BookFolderManager.write_new_folder(abs_p, self.proj_folder_manager.copy_folder_path, self.config.get_meta_scheme(), rel_p)
            res = self.preprocess_book(bfm)
            bfm.book_state.preprocessed = res
            bfm.save_book_state()
            count += 1
            yield count, total_amount
        pass

    def preprocess_book(self, book_folder_manager: BookFolderManager):
        self.logger.info('start preprocessing of a book at %s', str(book_folder_manager.temp_book_path))
        try:
            self._populate_temp_folder_with_pdf(book_folder_manager)
            if self.config.orc_config.do_ocr:
                self._apply_text_recognition(book_folder_manager)
        except PreprocessError as e:
            self.logger.warning(f'exception {e} while preprocessing book at {book_folder_manager.temp_book_path}')
            if self.config.stop_when_cant_preprocess:
                raise e
            return False
        return True

    def _populate_temp_folder_with_pdf(self, folder_manager: BookFolderManager):
        """copy book to temp if it is pdf; else convert and place in temp"""
        original = Path(self.project_dir,
                        folder_manager.original_relative_filepath)

        extension = original.suffix.strip('.')
        self.logger.debug(
            f'attempt to copy {extension} book from {original} to {folder_manager.temp_book_path}')
        if extension == 'pdf':
            self.logger.debug('copying pdf file')
            try:
                utils.copy_file(original, folder_manager.temp_book_path)
            except FileNotFoundError as e:
                raise PreprocessError(f"original file not found; path may be too long; path = {original}")
        elif extension == 'djvu':
            # todo: check if works with long paths
            self.logger.debug('converting djvu to pdf')
            try:
                djvu_to_pdf.convert_djvu_to_pdf(original, folder_manager.temp_book_path)
            except ChildProcessError as e:
                self.logger.warning(f'cant convert djvu to pdf at {original}')
                self.logger.debug(f'exception {e} raised')
                raise PreprocessError(e)
            except FileNotFoundError as e:
                self.logger.warning(f'original file not found; path may be too long; path={original}')
                self.logger.debug(f'exception {e} raised')
                raise PreprocessError(e)
            except EnvironmentError as e:
                self.logger.debug(f'exception {e} raised')
                raise PreprocessError(e)
            pass
        else:
            message = f'book files with {extension} extension not supported; got on file {original}'
            self.logger.warning(message)
            raise PreprocessError(message)
        pass

    def _apply_text_recognition(self, folder_manager: BookFolderManager):
        # todo: pages_arg may be None; how to achieve that?
        try:
            Recognizer.ocr(src_path=folder_manager.temp_book_path,
                           dst_path=folder_manager.temp_book_path,
                           language_arg=self.config.orc_config.language_arg,
                           pages_arg=self.config.orc_config.pages_arg)
        except EnvironmentError as e:
            self.logger.debug(f'caught {e} while applying OCR')
            raise PreprocessError(e)
        pass
