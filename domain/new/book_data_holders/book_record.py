import json
from pathlib import Path
from domain.new.description_stage import DescriptionStage


class BookRecord:
    def __init__(self, old_book_path, new_book_path, description_stage: DescriptionStage):
        self.old_book_path = Path(old_book_path)
        self.new_book_path = Path(new_book_path)
        self.description_stage = description_stage
        pass

    def __repr__(self):
        data = {'old_book_path': str(self.old_book_path),
                'new_book_path': str(self.new_book_path),
                'description_stage': str(self.description_stage)}
        return json.dumps(data)

    def __str__(self):
        return repr(self)

    @staticmethod
    def load_from_str(string):
        data = json.loads(string)
        return BookRecord(**data)
    pass
