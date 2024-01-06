import utils
from pathlib import Path


_root = Path('E:\ProjectLib\path_testing')


def make_long_directory_path_out_of_short(root):
    not_so_long_name = 'dir__that_has__very_long_name_40___symb_'
    long_dir_path = Path(root, *[not_so_long_name]*8)
    utils.make_directory(long_dir_path, parents=True)
    return long_dir_path


def make_short_named_file(folder: Path, text='wahaha'):
    filepath = Path(folder, 'short_file.txt')
    utils.write_text_to_file(filepath, text=text)
    return filepath


def make_long_long_dir(root: Path):
    long_name = '300 chars; that`s easy; let me tell you a story about a fish;' \
                ' once upon a time a fish lived in that old pond; ' \
                'its name was Tom; it lived a happy life with his family and friends' \
                'but time passed; years; decades; centuries; now pond is empty;' \
                'where is Tom, i wonder; where is that small fish which once lived here'
    dir_path = Path(root, long_name[:150], long_name[150:])
    utils.make_directory(dir_path, parents=True)
    return dir_path


def make_unicode_short_symbol_long_byte_file(root: Path):
    cur_len = len(str(root))
    if cur_len >= 240:
        raise ValueError('cant perform that test')
    filename = min((240 - cur_len - 3), 90) * '\u1f70'
    path = Path(root, filename)
    utils.write_text_to_file(filepath=path, text='some text')
    return path


def great_test(root: Path):
    long_short_dir = make_long_directory_path_out_of_short(root)
    print(f'made long path to dir out of short named dirs; pathlen = {len(str(long_short_dir))}')
    initial_text = 'text wahahaha'
    short_file_on_long_short_path = make_short_named_file(long_short_dir, text=initial_text)
    print(f'made short file of long_short path; pathlen = {len(str(short_file_on_long_short_path))}')
    text = utils.read_text_from_file(short_file_on_long_short_path)
    print(f'read short file on long_short path; text={text}')

    long_long_dir = make_long_long_dir(root)
    print(f'made long long dir; len = {len(str(long_long_dir))}')

    dst_long_long_file = Path(long_long_dir, short_file_on_long_short_path.name)
    utils.copy_file(short_file_on_long_short_path, dst_long_long_file)
    t = utils.read_text_from_file(dst_long_long_file)
    print(f'copied file from long short to long long; t = {t}')


    dst_top_file = Path(root, short_file_on_long_short_path.name)
    utils.move_file(short_file_on_long_short_path, dst_top_file)
    textt = utils.read_text_from_file(dst_top_file)
    print(f'lifted file from long_short to top level folder; textt = {textt}')

    uni_file_path = make_unicode_short_symbol_long_byte_file(root)
    print(f'made unicode short_but_not file; path len = {len(str(uni_file_path))};'
          f' path byte len = {len(str(uni_file_path).encode())}')
    tttt = utils.read_text_from_file(uni_file_path)
    print(f'read text from that file: text = {tttt}')
    pass


# great_test(_root)
