from pathlib import Path

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
        pass

    def preprocess_with_generator(self):
        """yields current preprocessed count and total amount"""
        abs_paths = LibScanner.find_all_files(self.config.extensions,
                                              lib_root_path=self.proj_folder_manager.lib_root_path)
        # todo: delegate state creation to project folder manager
        state = State.create_new(self.project_dir, abs_paths)
        state.dump_all()

        # todo: check if already preprocessed

        # todo: take those from state
        books_to_preprocess_paths = abs_paths

        count = 0
        total_amount = len(books_to_preprocess_paths)

        yield count, total_amount

        for p in books_to_preprocess_paths:
            self.preprocess_book(p)
            count += 1
            yield count, total_amount
        pass

    def preprocess_book(self, book_path: Path):
        folder_manager = BookFolderManager.create_folder_from(book_path, self.config)
        self._populate_temp_folder_with_pdf(folder_manager)
        self._apply_text_recognition(folder_manager)
        pass

    def _populate_temp_folder_with_pdf(self, folder_manager: BookFolderManager):
        """copy book to temp if it is pdf; else convert and place in temp"""
        original = folder_manager.original_book_path
        extension = original.suffix.strip('.')
        if extension == 'pdf':
            utils.copy_file(original, folder_manager.temp_book_path)
        elif extension == 'djvu':
            djvu_to_pdf.convert_djvu_to_pdf(original, folder_manager.temp_book_path)
            pass
        else:
            raise ValueError(f'book files with {extension} extension not supported; got on file {original}')
        pass

    def _apply_text_recognition(self, folder_manager: BookFolderManager):
        """after this method temp_book should contain text layer"""
        print(f'pretend to recognize text at {folder_manager.temp_book_path}')
        pass
    pass


proje_dir = r'E:\ProjectLib\result_root'


for cow, total in Preprocessor(proje_dir).preprocess_with_generator():
    print(f'{cow}/{total}')

