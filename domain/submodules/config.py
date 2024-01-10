from domain.field_config_record import FieldConfigRecord
from domain.book_data_holders.book_meta_scheme import BookMetaSchemeAdapter
from json.decoder import JSONDecodeError
import utils


class ConfigFormatError(ValueError):
    pass


class OCRConfig:
    _pages_arg_name = 'pages'
    _language_arg_name = 'language'
    _do_ocr_name = 'do_OCR'

    def __init__(self, pages_arg, language_arg, do_ocr):
        self.pages_arg = pages_arg
        self.language_arg = language_arg
        self.do_ocr = do_ocr
        pass

    @classmethod
    def load_from_dict(cls, ocr_data):
        return OCRConfig(pages_arg=ocr_data[cls._pages_arg_name],
                         language_arg=ocr_data[cls._language_arg_name],
                         do_ocr=ocr_data[cls._do_ocr_name])

    def dump_to_dict(self):
        ocr_data = dict()
        ocr_data[self._pages_arg_name] = self.pages_arg
        ocr_data[self._language_arg_name] = self.language_arg
        ocr_data[self._do_ocr_name] = self.do_ocr
        return ocr_data

    pass


class Config:
    _ocr_data_name = 'ocr_data'
    _lib_root_folder_name_name = 'lib_root_folder_name'
    _stop_when_cant_preprocess_name = 'stop_when_cant_preprocess'

    def __init__(self, fields: list, extensions: list, lib_root_folder_name, orc_config: OCRConfig, stop_when_cant_preprocess: bool):
        self.fields = fields
        self.extensions = extensions
        self.orc_config = orc_config
        self.lib_root_folder_name = lib_root_folder_name
        self.stop_when_cant_preprocess = stop_when_cant_preprocess
        pass

    def get_meta_scheme(self):
        return BookMetaSchemeAdapter(self.fields)

    def dumps(self):
        """use for default config generation maybe"""
        fields_data = {record.name:
                           {'human_readable_name': record.human_readable_name,
                            'readme_field_name': record.readme_field_name}
                       for record in self.fields}

        ocr_data = self.orc_config.dump_to_dict()

        data = {self._lib_root_folder_name_name: self.lib_root_folder_name,
                'extensions': self.extensions,
                self._stop_when_cant_preprocess_name: self.stop_when_cant_preprocess,
                'fields': fields_data,
                self._ocr_data_name: ocr_data}
        return utils.json_dumps(data)

    @classmethod
    def loads(cls, s):
        try:
            data = utils.json_loads(s)
        except JSONDecodeError:
            raise ConfigFormatError('config formatting is wrong; cannot read')
        try:
            lib_root_folder = data[cls._lib_root_folder_name_name]
            extensions = data['extensions']
            stop_when_cant_preprocess = data[cls._stop_when_cant_preprocess_name]
            # fixme: might fail when no readme mapping
            fields = [
                FieldConfigRecord(name=name,
                                  human_readable_name=content['human_readable_name'],
                                  readme_field_name=content['readme_field_name'])
                for name, content in data['fields'].items()
            ]

            ocr_data = data[cls._ocr_data_name]
            ocr_config = OCRConfig.load_from_dict(ocr_data)
        except KeyError:
            raise ConfigFormatError('config has some important data missing')
        return Config(fields=fields, extensions=extensions,
                      lib_root_folder_name=lib_root_folder,
                      orc_config=ocr_config,
                      stop_when_cant_preprocess=stop_when_cant_preprocess)

    @classmethod
    def get_default(cls):
        ocr_config = OCRConfig(pages_arg='1-5', language_arg='rus+eng',
                               do_ocr=False)
        conf = Config(
            [FieldConfigRecord('author', 'Автор', 'Author'),
             FieldConfigRecord('title', 'Название', 'Title'),
             FieldConfigRecord('publisher', 'Издатель', 'Publisher'),
             FieldConfigRecord('pages', 'Количество страниц', 'Pages'),
             FieldConfigRecord('year', 'Год издания', 'Year'),
             FieldConfigRecord('field_with_no_readme_field',
                               'Поле без соответствующего поля в README',
                               None)],
            ['.pdf', '.djvu'], lib_root_folder_name='lib_root',
            orc_config=ocr_config,
            stop_when_cant_preprocess=True)
        return conf
    pass
