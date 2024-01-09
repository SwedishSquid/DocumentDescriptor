from pathlib import Path

from domain.book_data_holders.description_stage import DescriptionStage
import utils


class BookState:
    """contains state of book nearby"""

    _original_rel_path_field_name = 'original_rel_path'
    _descr_stage_name = 'descr_stage'
    _preprocessed_name = 'preprocessed'
    # _from_folder_to_state ='temp/book_state.json'

    def __init__(self, original_rel_path: Path, descr_stage: DescriptionStage,
                 preprocessed: bool):
        """:param name: full name of book file"""
        self.original_rel_path = original_rel_path
        self.descr_stage = descr_stage
        self.preprocessed = preprocessed
        pass

    @classmethod
    def loads(cls, s):
        data = utils.json_loads(s)
        return BookState(Path(data[cls._original_rel_path_field_name]),
                         DescriptionStage(int(data[cls._descr_stage_name])),
                         data[cls._preprocessed_name])

    def dumps(self):
        data = {self._original_rel_path_field_name: str(self.original_rel_path),
                self._descr_stage_name: int(self.descr_stage),
                self._preprocessed_name: self.preprocessed}
        return utils.json_dumps(data)
    pass
