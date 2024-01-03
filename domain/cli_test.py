from domain.book_data_holders.book_info import BookInfo
from pathlib import Path
from domain.engine import Engine
from domain.book_data_holders.description_stage import DescriptionStage
from domain.preprocessor import Preprocessor
from domain.submodules.state import State


class CLI:
    def read_book_meta(self, info: BookInfo):
        meta = info.book_meta
        for name in meta.fields.keys():
            print(f'{name} aka {info.get_human_readable_name(name)} : {meta.fields[name]}', end='')
            plus = input()
            meta.fields[name] += plus
            # print()
        return meta

    def read_num(self):
        return int(input())

    def read_descr_stage(self):
        while True:
            print('put in description stage')
            print(f'1 == {DescriptionStage.IN_PROGRESS.name}')
            print(f'2 == {DescriptionStage.FINISHED.name}')
            print(f'3 == {DescriptionStage.REJECTED.name}')
            data = self.read_num()
            if data < 1 or data > 3:
                print('wrong input')
            else:
                return DescriptionStage(data)

    def run_description_mode(self, path: Path):
        print(f'start at {path}')
        engine = Engine(path)
        while True:
            book_info = engine.get_current_book()
            print(f'working on book at {book_info.absolute_path}')
            print(f'current stage is {book_info.description_stage.name}')
            meta = self.read_book_meta(book_info)
            d_stage = self.read_descr_stage()
            print(f'stage = {d_stage.name}')
            engine.save_book_data(meta, d_stage)
            print('saved')
            if not engine.try_set_book_index(engine.current_book_index + 1):
                break
        print('finished')
        pass

    def run_preprocessing_mode(self, path: Path):
        for cow, total in Preprocessor(path).preprocess_with_generator():
            print(f'{cow}/{total}')
        print('finished')
        pass

    def run(self, path: Path):
        if State.exists(path):
            print('state found; boot description')
            self.run_description_mode(path)
        else:
            print('state not found; begin preprocessing')
            self.run_preprocessing_mode(path)
        pass


path_to_proj = Path(r'E:\ProjectLib\result_root')
CLI().run(path_to_proj)
