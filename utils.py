from pathlib import Path
import shutil
import json


def write_text_to_file(filepath: Path, text: str, encoding='utf-8'):
    filepath.write_text(text, encoding=encoding)


def read_text_from_file(filepath: Path, encoding='utf-8'):
    return filepath.read_text(encoding=encoding)


def json_loads(s: str):
    return json.loads(s)


def json_dumps(obj, ensure_ascii=False, indent='    '):
    return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent)


def move_file(from_path: Path, to_path: Path):
    # todo: make move_file work with long filename (and test it)
    from_path.rename(to_path)
    pass


def make_directory(dir_path: Path):
    # todo: check if works with long paths; my guess is no
    dir_path.mkdir()
    pass


def copy_file(from_path: Path, to_path: Path):
    shutil.copyfile(src=str(from_path), dst=str(to_path))
    pass
