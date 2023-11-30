from domain.new.book_data_holders.book_meta import BookMeta


class BookMetaScheme:
    def __init__(self, name_to_human_read_plus_readme_pair: dict = None):
        self._name_to_data = dict()
        for name in name_to_human_read_plus_readme_pair:
            human_readable = name_to_human_read_plus_readme_pair[name][0]
            readme_readable = name_to_human_read_plus_readme_pair[name][1]
            self._add_field(name, human_readable, readme_readable)
        pass

    def _add_field(self, field_name: str,
                   human_readable_field_name: str,
                   readme_field_name: str = None):
        if field_name in self._name_to_data:
            raise KeyError(f'field {field_name} already added to book meta scheme')
        self._name_to_data[field_name] = (human_readable_field_name, readme_field_name)
        pass

    def make_book_meta_from_readme_data(self, readme_data: dict):
        data = dict()
        mapping = self.name_to_readme_name
        for field_name in mapping:
            if field_name in mapping:
                readme_field_name = mapping[field_name]
                if readme_field_name in readme_data:
                    data[field_name] = readme_data[readme_field_name]
                else:
                    data[field_name] = ''
            else:
                data[field_name] = ''
        return BookMeta(data)

    def make_empty_book_meta(self):
        return self.make_book_meta_from_readme_data(dict())

    @property
    def name_to_human_readable_name(self):
        data = dict()
        for name in self._name_to_data:
            data[name] = self._name_to_data[name][0]
        return data

    @property
    def name_to_readme_name(self):
        data = dict()
        for name in self._name_to_data:
            data[name] = self._name_to_data[name][1]
        return data

    @property
    def readme_name_to_name(self):
        data = dict()
        for name in self._name_to_data:
            readme_field_name = self._name_to_data[name][1]
            data[readme_field_name] = name
        return data
    pass
