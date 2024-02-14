from pathlib import Path

from domain.book_data_holders.description_stage import DescriptionStage
import utils


class BookState:
    """contains state of book nearby"""

    _original_rel_path_field_name = 'original_rel_path'
    _descr_stage_name = 'descr_stage'
    _preprocessed_name = 'preprocessed'
    _message_name = 'message'

    def __init__(self, original_rel_path: Path, descr_stage: DescriptionStage,
                 preprocessed: bool, message=None):
        self.original_rel_path = original_rel_path
        self.descr_stage = descr_stage
        self.preprocessed = preprocessed
        self.message = '' if message is None else message
        pass

    @classmethod
    def loads(cls, s):
        data = utils.json_loads(s)
        orig_path = Path(data[cls._original_rel_path_field_name])
        descr_stage = DescriptionStage(int(data[cls._descr_stage_name]))
        preprocessed = data[cls._preprocessed_name]
        message = None if cls._message_name not in data else data[cls._message_name]
        return BookState(original_rel_path=orig_path,
                         descr_stage=descr_stage,
                         preprocessed=preprocessed,
                         message=message)

    def dumps(self):
        data = {self._original_rel_path_field_name: str(self.original_rel_path),
                self._descr_stage_name: int(self.descr_stage),
                self._preprocessed_name: self.preprocessed,
                self._message_name: self.message}
        return utils.json_dumps(data)
    pass
