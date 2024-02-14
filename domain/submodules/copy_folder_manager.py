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
        # fixme: this sort thing might not be very consistent:
        #   ../book2 or ../book10, what shall go first?
        #   .glob thinks that book10; this sort on windows11 thinks that book2;
        #   for this app book2 is the right answer
        result.sort(key=lambda bfm: str(bfm.book_state.original_rel_path))
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
