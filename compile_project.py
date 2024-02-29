import PyInstaller.__main__
import resource_locator
import os
from pathlib import Path


"""run this on system under which need to compile into binaries
logs will be in ./build
results will be in ./dist"""


def _make_resource_arguments():
    p_sep = os.pathsep
    resources_folder_path = resource_locator.get_resource_folder()
    arguments = []
    for resource_file in resource_locator.get_all_resources_rel_paths():
        cur_file_path = resources_folder_path.joinpath(resource_file)
        bundled_file_dir_path = Path('resources', resource_file).parent
        arg = f'--add-data={cur_file_path}{p_sep}{bundled_file_dir_path}'
        arguments.append(arg)
    return arguments


def _make_icon_path():
    return resource_locator.get_resource_folder().joinpath('pictures/papyrus.ico')


def compile_descriptor_app():
    # full options list https://pyinstaller.org/en/stable/usage.html#options
    PyInstaller.__main__.run([
        'main.py',
        # '--onefile',
        '--name', 'descriptor',
        # '--noconsole',     # leaves only GUI; ignored on linux
        *_make_resource_arguments(),
        '--clean',      # means not to use cashed files
        '-y',       # replace previously compiled binary files in dist
        f'--icon={_make_icon_path()}',
    ])


def compile_preprocessor_app():
    PyInstaller.__main__.run([
        'run_preprocessor_cli.py',
        '--onefile',
        '--name', 'preprocessor'
    ])


if __name__ == '__main__':
    compile_descriptor_app()
    compile_preprocessor_app()
