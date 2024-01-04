import json


class BookMeta:
    def __init__(self, fields: dict, filename='book_meta.json'):
        self.fields = fields
        self._filename = filename
        pass

    def __repr__(self):
        return repr(self.fields)

    def __str__(self):
        return self.__repr__()

    def get_filename(self):
        return self._filename

    def dump_to_str(self):
        data = {'data': self.fields}
        return json.dumps(data, ensure_ascii=False, indent='    ')

    @staticmethod
    def load_from_str(str_data: str):
        data = json.loads(str_data)['data']
        return BookMeta(data)
    pass
