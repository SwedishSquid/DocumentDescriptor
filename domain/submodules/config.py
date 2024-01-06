import json
from domain.field_config_record import FieldConfigRecord
from domain.book_data_holders.book_meta_scheme import BookMetaSchemeAdapter


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

    def __init__(self, fields: list, extensions: list, lib_root_folder_name, orc_config: OCRConfig):
        self.fields = fields
        self.extensions = extensions
        self.orc_config = orc_config
        self.lib_root_folder_name = lib_root_folder_name
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

        data = {'lib_root_folder_name': self.lib_root_folder_name,
                'extensions': self.extensions,
                'fields': fields_data,
                self._ocr_data_name: ocr_data}
        return json.dumps(data, ensure_ascii=False, indent='    ')

    @classmethod
    def loads(cls, s):
        data = json.loads(s)
        extensions = data['extensions']
        # fixme: might fail when no readme mapping
        fields = [
            FieldConfigRecord(name=name,
                              human_readable_name=content['human_readable_name'],
                              readme_field_name=content['readme_field_name'])
            for name, content in data['fields'].items()
        ]

        ocr_data = data[cls._ocr_data_name]
        ocr_config = OCRConfig.load_from_dict(ocr_data)

        return Config(fields=fields, extensions=extensions,
                      lib_root_folder_name=data['lib_root_folder_name'],
                      orc_config=ocr_config)

    pass
