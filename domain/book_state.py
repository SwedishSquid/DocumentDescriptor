from pathlib import Path

from domain.book_data_holders.description_stage import DescriptionStage
import utils


class BookState:
    """contains state of book nearby"""

    _name_field_name = 'name'
    _descr_stage_name = 'descr_stage'
    # _from_folder_to_state ='temp/book_state.json'

    def __init__(self, name: str, descr_stage: DescriptionStage):
        """:param name: full name of book file"""
        self.name = name
        self.descr_stage = descr_stage
        pass

    # @classmethod
    # def load_from_book_folder(cls, folder_path):
    #     return cls.loads(utils.read_text_from_file(
    #         Path(folder_path, cls._from_folder_to_state))
    #     )

    @classmethod
    def load_from_file(cls, filepath: Path):
        return cls.loads(utils.read_text_from_file(filepath))

    @classmethod
    def loads(cls, s):
        data = utils.json_loads(s)
        return BookState(data[cls._name_field_name],
                         DescriptionStage(int(data[cls._descr_stage_name])))

    # def dump_to_book_folder(self, folder):
    #     utils.write_text_to_file(Path(folder, self._from_folder_to_state), self.dumps())
    #     pass

    def dump_to_file(self, filepath: Path):
        utils.write_text_to_file(filepath, self.dumps())
        pass

    def dumps(self):
        data = {self._name_field_name: self.name,
                self._descr_stage_name: int(self.descr_stage)}
        return utils.json_dumps(data)
    pass
