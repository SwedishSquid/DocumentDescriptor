from pathlib import Path


# https://pyinstaller.org/en/stable/runtime-information.html?#using-file

def get_resource_folder():
    return Path(__file__).resolve().with_name('resources')


def get_all_resources_rel_paths():
    """relative to resources dir
    needed for pyinstaller"""

    pic_dir = Path('pictures')
    pic_rel_paths = ['cross.svg', 'file.svg', 'folder.svg', 'right-arrow.svg']
    pictures = [pic_dir.joinpath(p) for p in pic_rel_paths]
    return pictures
