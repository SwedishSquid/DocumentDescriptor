from pathlib import Path

from domain.converters.recognizer import Recognizer

from domain.book_data_holders.book_folder_manager import BookFolderManager
from domain.converters import djvu_to_pdf
from domain.submodules.project_folder_manager import ProjectFolderManager
import utils


class PreprocessError(Exception):
    """raise when can`t preprocess document"""


class Preprocessor:
    def __init__(self, project_folder_manager: ProjectFolderManager):
        self.proj_folder_manager = project_folder_manager
        self.project_dir = self.proj_folder_manager.project_folder
        self.config = self.proj_folder_manager.config
        pass

    def preprocess_with_generator(self, original_books_to_preprocess: list, ms_receiver=None):
        """yields current preprocessed count and total amount"""
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)

        count = 0
        total_amount = len(original_books_to_preprocess)

        yield count, total_amount

        for abs_p in original_books_to_preprocess:
            rel_p = self.proj_folder_manager.make_relative_path(abs_p)
            bfm = BookFolderManager.write_new_folder(abs_p, self.proj_folder_manager.copy_folder_path, self.config.get_meta_scheme(), rel_p)
            res = self.preprocess_book(bfm, ms_receiver)
            bfm.book_state.preprocessed = res
            bfm.save_book_state()
            count += 1
            yield count, total_amount
        pass

    def preprocess_book(self, book_folder_manager: BookFolderManager, ms_receiver=None):
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)
        try:
            self._populate_temp_folder_with_pdf(book_folder_manager, ms_receiver)
            if self.config.orc_config.do_ocr:
                self._apply_text_recognition(book_folder_manager)
        except PreprocessError as e:
            ms_receiver(str(e))
            if self.config.stop_when_cant_preprocess:
                raise e
            return False
        return True

    def _populate_temp_folder_with_pdf(self, folder_manager: BookFolderManager, ms_receiver=None):
        """copy book to temp if it is pdf; else convert and place in temp"""
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)
        original = Path(self.project_dir,
                        folder_manager.original_relative_filepath)

        extension = original.suffix.strip('.')
        if extension == 'pdf':
            try:
                utils.copy_file(original, folder_manager.temp_book_path)
            except FileNotFoundError as e:
                raise PreprocessError(f"original file not found; path may be too long; path = {original}")
        elif extension == 'djvu':
            # todo: check if works with long paths
            try:
                djvu_to_pdf.convert_djvu_to_pdf(original, folder_manager.temp_book_path)
            except ChildProcessError as e:
                ms_receiver(f'cant convert djvu to pdf at {original}')
                raise PreprocessError(e)
            except FileNotFoundError as e:
                ms_receiver(f'original file not found; path may be too long; path={original}')
                raise PreprocessError(e)
            except EnvironmentError as e:
                ms_receiver(str(e))
                raise PreprocessError(e)
            pass
        else:
            message = f'book files with {extension} extension not supported; got on file {original}'
            ms_receiver(message)
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
            raise PreprocessError(e)
        pass
