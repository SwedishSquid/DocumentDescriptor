from pathlib import Path
from domain.book_data_holders.book_meta import BookMeta


class MetaFilehandler:
    filename = 'book_meta.json'
    encoding = 'utf-8'

    def write_book_meta(self, book_meta: BookMeta, path_to_book_dir):
        path = self._make_path(path_to_book_dir)
        # todo: replace with utils call (if it is still in use)
        path.write_text(book_meta.dump_to_str(), encoding=self.encoding)
        pass

    def read_from_file(self, path_to_book_dir):
        path = self._make_path(path_to_book_dir)
        # todo: replace with utils call
        str_data = path.read_text(encoding=self.encoding)
        return BookMeta.load_from_str(str_data)

    def _make_path(self, path_to_book_dir):
        path = Path(path_to_book_dir)
        if not path.is_dir():
            raise ValueError(
                f'path_to_book_dir is not a directory: {path_to_book_dir}')
        path = Path(path, self.filename)
        return path
    pass
