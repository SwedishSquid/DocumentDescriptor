import json
from pathlib import Path
from domain.book_data_holders.description_stage import DescriptionStage


class WorkstateBookRecord:
    def __init__(self, current_book_path, old_book_path,
                 description_stage: DescriptionStage):
        self.book_path = Path(current_book_path)
        self.old_book_path: Path = self.book_path if old_book_path is None else Path(
            old_book_path)
        self.description_stage = DescriptionStage(int(description_stage))
        pass

    def __repr__(self):
        data = {
            'current_book_path': str(self.book_path),
            'old_book_path': str(self.old_book_path),
            'description_stage': str(self.description_stage)
        }
        return json.dumps(data)

    def __str__(self):
        return repr(self)

    def __copy__(self):
        return WorkstateBookRecord.load_from_str(repr(self))

    @staticmethod
    def load_from_str(string):
        data = json.loads(string)
        return WorkstateBookRecord(**data)

    pass
