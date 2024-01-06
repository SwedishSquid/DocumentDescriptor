from pathlib import Path

import utils
from domain.book_data_holders.book_meta import BookMeta


class MetaFilehandler:
    filename = 'book_meta.json'
    encoding = 'utf-8'

    def write_book_meta(self, book_meta: BookMeta, path_to_book_dir):
        path = self._make_path(path_to_book_dir)
        utils.write_text_to_file(path, book_meta.dump_to_str())
        pass

    def read_from_file(self, path_to_book_dir):
        path = self._make_path(path_to_book_dir)
        str_data = utils.read_text_from_file(path)
        return BookMeta.load_from_str(str_data)

    def _make_path(self, path_to_book_dir):
        path = Path(path_to_book_dir)
        if not utils.is_dir(path):
            raise ValueError(
                f'path_to_book_dir is not a directory: {path_to_book_dir}')
        path = Path(path, self.filename)
        return path
    pass
