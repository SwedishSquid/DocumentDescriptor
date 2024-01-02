import pathlib
import unittest
import shutil
import ocrmypdf
from pathlib import Path

from app.adapters.djvu_to_pdf_converter import DjvuPdfConverter
from domain.engine import Engine
from domain.submodules.workstate.work_state import WorkState


class TestEngine(unittest.TestCase):
    path_to_test_cases = Path(r"D:\InterestingStuff\DocDescriptorLib\test_cases")
    current_lib: Path = None

    # def setUp(self):
    #     self.engine = Engine(self.path_to_proj)

    # def tearDown(self):
    #     shutil.rmtree(self.current_lib.absolute(), ignore_errors=False)
    #     pass

    # need to create temp copy of testing lib
    def test_empty_workstate_updated_correctly(self):
        rel_test_lib_path = Path("test_workstate_update")
        abs_test_lib_path = Path(self.path_to_test_cases, rel_test_lib_path)
        self.get_lib_copy(abs_test_lib_path)
        # engine = Engine(abs_test_lib_path)
        # raise NotImplementedError()
        pass

    def test_prepare_book(self):
        rel_test_lib_path = Path("test_prepare_book")
        abs_test_lib_path = Path(self.path_to_test_cases, rel_test_lib_path)
        self.get_lib_copy(abs_test_lib_path)
        # engine = Engine(abs_test_lib_path)
        # raise NotImplementedError()
        pass

    def test_readme_reader(self):
        raise NotImplementedError()
        # pass

    # def test_cli_workflow(self):
    #     engine = Engine(self.path_to_proj)
    #     book_info = self.engine.get_current_book()
    #     print(f'working on book at {book_info.absolute_path}')
    #     print(f'current stage is {book_info.description_stage.name}')
    #     meta = self.read_book_meta(book_info)
    #     d_stage = self.read_descr_stage()
    #     print(f'stage = {d_stage.name}')
    #     engine.save_book_data(meta, d_stage)
    #     print('saved')
    #     if not engine.try_set_book_index(engine.current_book_index + 1):
    #         break

    def get_lib_copy(self, lib_path: Path):
        source_dir = lib_path
        destination_dir = Path(lib_path.parent, Path(lib_path.name.__str__() + "_temp"))
        shutil.copytree(source_dir, destination_dir)
        self.current_lib = destination_dir

    def test_ocr_pdf(self):
        rel_test_lib_path = Path("test_ocrmypdf")
        abs_test_lib_path = Path(self.path_to_test_cases, rel_test_lib_path)
        djvu_converter = DjvuPdfConverter(abs_test_lib_path)
        engine = Engine(abs_test_lib_path)
        book_info = engine.get_current_book()
        if book_info.absolute_path.suffix == '.djvu':
            if not djvu_converter.try_replace_djvu_book_with_pdf_clone(book_info):
                raise ChildProcessError(f'can not convert djvu to pdf. initial file at {book_info.absolute_path}')
        else:
            pass
        pass



if __name__ == '__main__':
    unittest.main()
