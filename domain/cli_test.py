from domain.new.book_data_holders.book_meta import BookMeta
from pathlib import Path
from domain.new.engine import Engine
from domain.new.book_data_holders.description_stage import DescriptionStage


class CLI:
    def read_book_meta(self, meta: BookMeta):
        for k in meta.fields:
            print(f'{k} : {meta.fields[k]}', end='')
            plus = input()
            meta.fields[k] += plus
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

    def run(self, path: Path):
        print(f'start at {path}')
        engine = Engine(path)
        while True:
            p, meta = engine.get_current_book()
            print(f'working on book at {p}')
            meta = self.read_book_meta(meta)
            d_stage = self.read_descr_stage()
            print(f'stage = {d_stage.name}')
            engine.save_book_data(meta, d_stage)
            print('saved')
            if not engine.try_set_book_index(engine.current_book_index + 1):
                break
        print('finished')
        pass


path_to_proj = Path(r'E:\ProjectLib\result_root')
CLI().run(path_to_proj)
