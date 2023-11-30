from pathlib import Path
import json
from domain.new.book_data_holders.book_record import BookRecord
from domain.new.description_stage import DescriptionStage


class WorkState:
    records_list_name = 'book_records_list'

    def __init__(self, book_records: list):
        self._book_records = book_records
        # self._new_paths_to_stage = dict()
        # for record in self._book_records:
        #     self._new_paths_to_stage[record.new_book_path] = record.description_stage
        pass

    @property
    def book_records(self):
        return self._book_records

    # @property
    # def new_paths_to_stage_mapping(self):
    #     return self._new_paths_to_stage

    def update_with_paths(self, paths):
        new_paths_to_records = dict()
        for record in self._book_records:
            if record.description_stage == DescriptionStage.NOT_STARTED:
                continue
            new_paths_to_records[str(record.new_book_path)] = record
        result_records = []
        for path in paths:
            if str(path) in new_paths_to_records:
                result_records.append(new_paths_to_records[str(path)])
            else:
                result_records.append(BookRecord(path, None, DescriptionStage.NOT_STARTED))
        self._book_records = result_records
        pass

    def dump_to_file(self, path_to_file):
        path = Path(path_to_file)
        # if not path.is_file():
        #     raise ValueError(f'{path} is not a file')
        data = {self.records_list_name: [str(record)
                                         for record in self._book_records]}
        path.write_text(json.dumps(data))
        pass

    @classmethod
    def load_from_file(cls, path_to_file):
        path = Path(path_to_file)
        if not path.is_file():
            raise ValueError(f'{path} is not a file')
        data = json.loads(path.read_text())
        records = [BookRecord.load_from_str(record_str)
                   for record_str in data[cls.records_list_name]]
        return WorkState(records)
    pass
