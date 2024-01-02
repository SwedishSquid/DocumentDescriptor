import json
from domain.field_config_record import FieldConfigRecord
from domain.book_data_holders.book_meta_scheme import BookMetaSchemeAdapter


class Config:
    # filename = 'config.json'

    def __init__(self, fields: list, extensions: list, lib_root_folder_name):
        self.fields = fields
        self.extensions = extensions
        self.lib_root_folder_name = lib_root_folder_name
        pass

    def get_meta_scheme(self):
        return BookMetaSchemeAdapter(self.fields)

    def _dumps(self):
        """use for default config generation maybe"""
        fields_data = {record.name:
                           {'human_readable_name': record.human_readable_name,
                            'readme_field_name': record.readme_field_name}
                       for record in self.fields}

        data = {'lib_root_folder_name': self.lib_root_folder_name,
                'extensions': self.extensions, 'fields': fields_data}
        return json.dumps(data, ensure_ascii=False, indent='    ')

    @staticmethod
    def loads(s):
        data = json.loads(s)
        extensions = data['extensions']
        # fixme: fails when no readme mapping
        fields = [
            FieldConfigRecord(name=name,
                              human_readable_name=content['human_readable_name'],
                              readme_field_name=content['readme_field_name'])
            for name, content in data['fields'].items()
        ]
        return Config(fields=fields, extensions=extensions,
                      lib_root_folder_name=data['lib_root_folder_name'])

    pass
