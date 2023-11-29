from pathlib import Path
from domain.new.config_handler.my_config_reader import MyConfigReader
# from book_meta_scheme import BookMetaScheme


class Model:
    workstate_file_name = 'workstate.json'
    config_file_name = 'config.json'
    result_book_cluster_name = 'result_cluster'

    def __init__(self, lib_root, result_root):
        self.lib_root = Path(lib_root)
        self._check_if_dir(self.lib_root)

        self.result_root = Path(result_root)
        self._check_if_dir(self.result_root)

        self.config_path = self.result_root.joinpath(self.config_file_name)
        self.workstate_path = self.result_root.joinpath(self.workstate_file_name)
        self.book_cluster_path = self.result_root.joinpath(self.result_book_cluster_name)

        self.scheme = self._load_scheme()

        self.relative_to_lib_root_source_books_paths = self._scan_source_lib()
        pass

    def _scan_source_lib(self):
        patterns = ['*.djvu', '*.pdf']
        absolute_paths = []
        for pattern in patterns:
            for p in self.lib_root.rglob(pattern):
                if p.is_file():
                    absolute_paths.append(p)
        relative_paths = [Path(*p.parts[len(self.lib_root.parts):]) for p in absolute_paths]
        return relative_paths

    def _load_scheme(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f'config file not found at {self.config_path}')
        return MyConfigReader(self.config_path).get_book_meta_scheme()

    def _check_if_dir(self, path: Path):
        if not path.is_dir():
            raise ValueError(f'{path} is not a directory or not exists')
        pass
    pass
