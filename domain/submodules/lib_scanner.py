from pathlib import Path


class LibScanner:
    @staticmethod
    def find_all_files(extensions, lib_root_path):
        """gets absolute path to every file of listed extension
        :param lib_root_path: root of library piece; NOT a project root !!!"""
        lib_root_path = Path(lib_root_path)
        extensions = [str(x).strip('.') for x in extensions]
        patterns = [f'*.{x}' for x in extensions]
        absolute_paths = []
        for pattern in patterns:
            for p in lib_root_path.rglob(pattern):
                if p.is_file():
                    absolute_paths.append(p)
        return absolute_paths
    pass
