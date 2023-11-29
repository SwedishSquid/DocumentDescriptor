from pathlib import Path
from workstate_handler.work_state import WorkState


class Engine:
    config_file_name = 'config.json'
    lib_dir_name = 'lib_root'
    workstate_file_name = 'workstate.json'

    def __init__(self, project_directory, lib_dir_name=None):
        self.project_directory = Path(project_directory)
        if not self.project_directory.is_dir():
            raise NotADirectoryError(f'{self.project_directory} is not a directory')
        if lib_dir_name is not None:
            self.lib_dir_name = lib_dir_name

        self.config_path = Path(self.project_directory, self.config_file_name)
        if not self.config_path.exists():
            raise FileNotFoundError(f'{self.config_path} config file not found')

        self.lib_root_path = Path(self.project_directory, self.lib_dir_name)
        if not self.lib_root_path.exists():
            raise FileNotFoundError(f'{self.lib_root_path} not found')
        if not self.lib_root_path.is_dir():
            raise NotADirectoryError(f'{self.lib_root_path} is not a directory')

        self.workstate_path = Path(self.project_directory, self.workstate_file_name)
        if not self.workstate_path.exists():
            self.workstate = WorkState([])
        else:
            self.workstate = WorkState.load_from_file(self.workstate_path)
        pass

    def _scan_lib(self):
        '''get relative paths from lib_root to every file of book-like extension'''
        patterns = ['*.djvu', '*.pdf']
        absolute_paths = []
        for pattern in patterns:
            for p in self.lib_root_path.rglob(pattern):
                if p.is_file():
                    absolute_paths.append(p)
        relative_paths = [Path(*p.parts[len(self.lib_root_path.parts):]) for p in
                          absolute_paths]
        return relative_paths
    pass
