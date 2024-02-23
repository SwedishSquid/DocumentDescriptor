from pathlib import Path
from domain.book_data_holders.book_folder_manager import BookFolderManager
import utils


class CopyFolderManager:
    def __init__(self, copy_folder_path: Path):
        self.copy_folder_path = copy_folder_path
        pass

    def load_book_folders_managers(self, ms_receiver=None):
        if ms_receiver is None:
            ms_receiver = lambda s: print(s)

        result = []

        for path in self._get_all_subpaths():
            if utils.is_dir(path):
                bfm = BookFolderManager.load_from_path(path, ms_receiver)
                if bfm and bfm.book_state.preprocessed:
                    result.append(bfm)
        result.sort(key=lambda bfm: bfm.sequence_number)
        return result

    def _get_all_subpaths(self):
        for path in self.copy_folder_path.glob('*'):
            yield path

    def delete_all_not_preprocessed_bfm(self):
        for path in self._get_all_subpaths():
            if utils.is_dir(path):
                bfm = BookFolderManager.load_from_path(path)
                if bfm and bfm.book_state.preprocessed:
                    continue
            utils.delete_from(path)
        pass
    pass
