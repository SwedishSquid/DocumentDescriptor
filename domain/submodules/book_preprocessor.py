from domain.submodules.readme_reader import ReadmeReader
from domain.submodules.workstate.workstate_book_record import WorkstateBookRecord
from domain.book_data_holders.description_stage import DescriptionStage
from pathlib import Path
from domain.book_data_holders.book_meta_scheme import BookMetaScheme


class BookPreprocessor:
    """use this to prepare book file and gather information from README
     before showing file to operator """

    readme_file_name = 'README'

    def __init__(self, lib_root_path, readme_reader: ReadmeReader,
                 meta_scheme: BookMetaScheme):
        self.readme_reader = readme_reader
        self.lib_root_path = Path(lib_root_path)
        self.scheme = meta_scheme
        pass

    def preprocess(self, workstate_record: WorkstateBookRecord):
        """save workstate and acquired meta afterwords"""
        if workstate_record.description_stage != DescriptionStage.NOT_STARTED:
            raise ValueError(f'attempted to preprocess already prepared book')
        abs_old_book_path = Path(self.lib_root_path, workstate_record.book_path)
        abs_old_dir_path = abs_old_book_path.parent
        abs_readme_path = Path(abs_old_dir_path, self.readme_file_name)
        if abs_readme_path.exists() and abs_readme_path.is_file():
            result_meta = self.readme_reader.read(abs_readme_path)
        else:
            result_meta = self.scheme.make_empty_book_meta()
        self._move_book_file(workstate_record)
        return result_meta

    def _move_book_file(self, workstate_record: WorkstateBookRecord):
        """перемещает файл книги в иерархии файлов на уровень ниже,
        в папку с названием как у файла книги"""
        relative_dir_path = workstate_record.book_path.with_suffix('')
        abs_dir_path = Path(self.lib_root_path, relative_dir_path)
        if not abs_dir_path.exists():
            abs_dir_path.mkdir()
        rel_new_book_path = Path(relative_dir_path, workstate_record.book_path.name)
        rel_old_book_path = workstate_record.book_path
        workstate_record.book_path = rel_new_book_path
        # move
        abs_new_book_path = Path(self.lib_root_path, rel_new_book_path)
        abs_old_book_path = Path(self.lib_root_path, rel_old_book_path)
        abs_old_book_path.rename(abs_new_book_path)     # this line moves file
        workstate_record.description_stage = DescriptionStage.IN_PROGRESS
        return workstate_record
    pass
