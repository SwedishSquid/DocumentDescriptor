import utils


class BookMeta:
    _fields_section_name = 'data'
    _initial_filename_section_name = 'initial_filename'

    def __init__(self, fields: dict, initial_file_name: str = ''):
        self.fields = fields
        self.initial_file_name = initial_file_name
        pass

    def __repr__(self):
        return repr(self.fields)

    def __str__(self):
        return self.__repr__()

    def dump_to_str(self):
        data = {self._fields_section_name: self.fields,
                self._initial_filename_section_name: self.initial_file_name}
        return utils.json_dumps(data)

    @classmethod
    def load_from_str(cls, str_data: str):
        data = utils.json_loads(str_data)
        fields = data[cls._fields_section_name]
        initial_file_name = data[cls._initial_filename_section_name]
        return BookMeta(fields, initial_file_name=initial_file_name)

    pass
