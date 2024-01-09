from pathlib import Path
from domain.book_data_holders.book_folder_manager import BookFolderManager
import utils


class State:
    _state_folder_name = 'state'
    _book_folders_filename = 'book_folders.json'
    _dynamic_state_filename = 'dynamic_state.json'

    _book_folders_key = 'book_folders'
    _index_key = 'index'

    def __init__(self, project_path):
        """caution: resource intensive operation
        collects every book state in library"""
        self.project_path = Path(project_path)
        if not self.project_path.exists() or not self.project_path.is_dir():
            raise NotADirectoryError(f'project path must be a directory and exist; got {self.project_path}')

        self.book_folders = self._load_book_folders()

        self.book_folders_managers = [BookFolderManager(bf)
                                      for bf in self.book_folders]

        # fixme: index not working and not saving when run via main
        self.index = self._load_index()
        pass

    def save_index(self, index):
        self.index = index
        dynamic_state_filepath = Path(self.project_path,
                                      self._state_folder_name,
                                      self._dynamic_state_filename)
        dynamic_data = {self._index_key: self.index}
        utils.write_text_to_file(dynamic_state_filepath,
                                 utils.json_dumps(dynamic_data))
        pass

    def _load_book_folders(self):
        """:returns: absolute paths to book folders"""
        book_folders_path = Path(self.project_path,
                                 self._state_folder_name,
                                 self._book_folders_filename)
        data = utils.json_loads(utils.read_text_from_file(book_folders_path))
        return [Path(self.project_path, p_str) for p_str in data[self._book_folders_key]]

    def _load_index(self):
        dynamic_state_path = Path(self.project_path,
                                  self._state_folder_name,
                                  self._dynamic_state_filename)
        data = utils.json_loads(utils.read_text_from_file(dynamic_state_path))
        return int(data[self._index_key])

    @classmethod
    def exists(cls, project_path: Path):
        # todo: make more reliable check
        return Path(project_path, cls._state_folder_name).exists()

    @classmethod
    def create_new(cls, project_path, book_folders_paths: list):
        """takes absolute paths to books' folders"""
        if cls.exists(project_path):
            raise FileExistsError('state already exists')
        utils.make_directory(Path(project_path, cls._state_folder_name))

        rel_paths = cls._make_relative_paths(project_path, book_folders_paths)
        book_folders_filepath = Path(project_path,
                                     cls._state_folder_name,
                                     cls._book_folders_filename)
        folders_paths_data = {cls._book_folders_key: [str(p) for p in rel_paths]}
        utils.write_text_to_file(book_folders_filepath,
                                 utils.json_dumps(folders_paths_data))

        index = 0
        dynamic_state_filepath = Path(project_path,
                                      cls._state_folder_name,
                                      cls._dynamic_state_filename)
        dynamic_data = {cls._index_key: index}
        utils.write_text_to_file(dynamic_state_filepath,
                                 utils.json_dumps(dynamic_data))
        return State(project_path=project_path)

    @classmethod
    def _make_relative_paths(cls, project_path, book_folders_paths: list):
        project_path = Path(project_path)
        if not project_path.is_absolute():
            raise ValueError('project_path must be absolute')
        proj_path_parts_len = len(project_path.parts)
        rel_paths = []
        for p in book_folders_paths:
            p = Path(p)
            if not Path(*p.parts[:proj_path_parts_len]).match(
                    str(project_path)):
                raise ValueError(
                    f'book folders must be inside project folder; proj: {project_path}; book_folder: {p}')
            rel_paths.append(Path(*p.parts[proj_path_parts_len:]))
        return rel_paths
    pass
