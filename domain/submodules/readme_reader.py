import codecs
import re
from domain.book_data_holders.book_meta_scheme import BookMetaScheme


class ReadmeReader:
    def __init__(self, meta_scheme: BookMetaScheme, encoding='koi8-r'):
        self.scheme = meta_scheme
        self.encoding = encoding
        pass

    def read(self, path_to_readme):
        with codecs.open(path_to_readme, 'r', self.encoding) as f:
            readme_text = f.read()
        # print(readme_text)
        m = re.findall(r'(.+?):(.+)', readme_text)
        readme_data = dict()
        for readme_field_name, readme_field_value in m:
            name = readme_field_name.strip(' \n\r\t')
            value = readme_field_value.strip(' \n\r\t')
            readme_data[name] = value
        return self.scheme.make_book_meta_from_readme_data(readme_data)
    pass

