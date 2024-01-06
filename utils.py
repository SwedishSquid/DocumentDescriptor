from pathlib import Path
import shutil
import json
import platform


def _make_long_path(path: Path):
    """use externally only if you very sure that it must be used. pls"""
    if platform.system().lower() != 'windows':
        return path
    s = str(path)
    if len(s) < 240:    # 255 is the limit though
        return path
    prefix = '\\\\?\\'
    if s.startswith(prefix):
        return path
    return Path(prefix + s)


def is_file(filepath: Path):
    filepath = _make_long_path(filepath)
    return filepath.is_file()


def is_dir(path: Path):
    path = _make_long_path(path)
    return path.is_dir()


def exists(path: Path):
    path = _make_long_path(path)
    return path.exists()


def write_text_to_file(filepath: Path, text: str, encoding='utf-8'):
    filepath = _make_long_path(filepath)
    filepath.write_text(text, encoding=encoding)


def read_text_from_file(filepath: Path, encoding='utf-8'):
    filepath = _make_long_path(filepath)
    return filepath.read_text(encoding=encoding)


def json_loads(s: str):
    return json.loads(s)


def json_dumps(obj, ensure_ascii=False, indent='    '):
    return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent)


def move_file(from_path: Path, to_path: Path):
    from_path = _make_long_path(from_path)
    to_path = _make_long_path(to_path)
    from_path.rename(to_path)
    pass


def make_directory(dir_path: Path, parents=False):
    dir_path = _make_long_path(dir_path)
    dir_path.mkdir(parents=parents)
    pass


def copy_file(from_path: Path, to_path: Path):
    from_path = _make_long_path(from_path)
    to_path = _make_long_path(to_path)
    shutil.copyfile(src=str(from_path), dst=str(to_path))
    pass
