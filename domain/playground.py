import json
import pathlib
import readme_reader
from domain.new.config_handler.my_config_reader import MyConfigReader
from meta_filehandler import MetaFilehandler

path = pathlib.Path(r'E:\dev\DocumentDescriptor\DocumentDescriptor\dir_that_git_ignores\config.json')
dir_path = path.parent


def write_conf():
    conf_data = {'field_section': {
        'author': ['автор', 'Author'],
        'title': ['название', 'Title'],
        'translator': ['переводчик', 'Translator'],
        'publisher': ['издатель', 'Publisher'],
        'year': ['год', 'Year'],
        'pages': ['страницы', 'Pages'],
        'noname': ['noname test field', None]
    }}
    s = json.dumps(conf_data)
    path.write_text(s)


def read_conf():
    data = path.read_text()
    s = json.loads(data)
    print(s)


def do_stuff():
    sch = MyConfigReader(path).get_book_meta_scheme()
    r = readme_reader.ReadmeReader(sch)
    res = r.read(r"E:\ProjectLib\libr\programming ПРОГРАММИРОВАНИЕ\Вирт Н. Алгоритмы и структуры данных\README")
    print(res)
    filehandler = MetaFilehandler()
    filehandler.write_book_meta(res, dir_path)
    pass


def read_meta_from_file():
    filehandler = MetaFilehandler()
    meta = filehandler.read_from_file(dir_path)
    print(meta)
    pass


def write_work_state():
    state_data = {'source_and_result_book_mapping': [
        {'source': 'source path', 'result': 'result path'}
    ]}
    s = json.dumps(state_data)
    dir_path.joinpath('workstate.json').write_text(s)
    pass

# read_conf()
# write_conf()

# do_stuff()

# read_meta_from_file()
# write_work_state()


def do_pathlib_stuff():
    root = pathlib.Path(r'E:\dev\DocumentDescriptor\DocumentDescriptor')
    print(path.is_relative_to(root))
    subpath = pathlib.Path(*path.parts[len(root.parts):])
    print(subpath.name)
    pass


do_pathlib_stuff()
