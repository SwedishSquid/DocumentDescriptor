class FieldConfigRecord:
    """contains information about field in meta file
    fields name, a nickname to show operator, and mapping to readme field, if has one"""

    def __init__(self, name, human_readable_name, readme_field_name):
        self.name = name
        self.human_readable_name = human_readable_name
        self.readme_field_name = readme_field_name
        pass
    pass
