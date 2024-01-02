from pathlib import Path
import json
from collections import namedtuple
from domain.book_data_holders.description_stage import DescriptionStage


BookStateRecord = namedtuple('BookStateRecord', 'rel_folder_path descr_stage')


class State:
    encoding = 'utf-8'

    def __init__(self, project_path, book_index, records: list):
        self.project_path = Path(project_path)
        self.state_file_path = Path(project_path, 'state.json')
        self.book_index = book_index
        self._records = records
        pass

    @classmethod
    def load(cls, project_path):
        state_file_path = Path(project_path, 'state.json')
        return cls._loads(state_file_path.read_text(encoding=cls.encoding),
                          project_path=project_path)

    @staticmethod
    def _loads(s, project_path):
        data = json.loads(s)
        records = [BookStateRecord(rel_folder_path=Path(r['rel_folder_path']),
                                   descr_stage=DescriptionStage(r['descr_stage']))
                   for r in data['records']]
        return State(project_path=project_path, book_index=data['book_index'],
                     records=records)

    @classmethod
    def create_new(cls, project_path, book_folders_paths: list):
        """takes absolute paths to books' folders
        ! don't forget to save"""
        rel_paths = cls._make_relative_paths(project_path, book_folders_paths)
        records = [BookStateRecord(rel_folder_path=p,
                                   descr_stage=DescriptionStage.NOT_STARTED)
                   for p in rel_paths]
        return State(project_path=project_path, book_index=0, records=records)

    def add_books(self, book_folders):
        raise NotImplementedError('have some trouble making that one; how to detect what books were already prepared? to delegate!')

    @classmethod
    def _make_relative_paths(cls, project_path, book_folders_paths: list):
        project_path = Path(project_path)
        if not project_path.is_absolute():
            raise ValueError('project_path must be absolute')
        proj_path_parts_len = len(project_path.parts)
        rel_paths = []
        for p in book_folders_paths:
            p = Path(p)
            if not Path(*p.parts[:proj_path_parts_len]).match(
                    str(project_path)):
                raise ValueError(
                    f'book folders must be inside project folder; proj: {project_path}; book_folder: {p}')
            rel_paths.append(Path(*p.parts[proj_path_parts_len:]))
        return rel_paths

    def dump_all(self):
        self.state_file_path.write_text(self._dumps_all(), encoding=self.encoding)
        pass

    def _dumps_all(self):
        data = {'book_index': self.book_index,
                'records': [{'rel_folder_path': str(record.rel_folder_path),
                             'descr_stage': record.descr_stage}
                            for record in self._records]}
        s = json.dumps(data, ensure_ascii=False, indent='    ')
        return s
    pass
