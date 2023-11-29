import json
from pathlib import Path
from domain.new.book_data_holders.book_meta_scheme import BookMetaScheme


class MyConfigReader:
    _field_section_name = 'field_section'

    def __init__(self, path):
        self.path = Path(path)
        self.config_data = json.loads(self.path.read_text())
        pass

    def get_book_meta_scheme(self):
        scheme = BookMetaScheme(self.config_data[self._field_section_name])
        return scheme
    pass
