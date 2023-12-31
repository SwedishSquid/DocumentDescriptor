import json
from pathlib import Path
from domain.book_data_holders.book_meta_scheme import BookMetaScheme


# fixme: конфиг неразрывно связан с читалкой
class MyConfigReader:
    _field_section_name = 'field_section'

    def __init__(self, path_to_config_file):
        self.path = Path(path_to_config_file)
        self.config_data = json.loads(self.path.read_text())
        pass

    def get_book_meta_scheme(self):
        scheme = BookMetaScheme(self.config_data[self._field_section_name])
        return scheme
    pass
