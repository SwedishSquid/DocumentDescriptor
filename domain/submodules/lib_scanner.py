from pathlib import Path


class LibScanner:
    def find_all_files(self, extensions, root_path):
        """gets absolute path to every file of listed extension"""
        root_path = Path(root_path)
        patterns = [f'*.{x}' for x in extensions]
        absolute_paths = []
        for pattern in patterns:
            for p in root_path.rglob(pattern):
                if p.is_file():
                    absolute_paths.append(p)
        return absolute_paths
    pass
