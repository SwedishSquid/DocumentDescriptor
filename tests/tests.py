import unittest
from pathlib import Path

from domain.preprocessor import Preprocessor

# todo: make more tests


class MyTestCase(unittest.TestCase):

    def test_make_recognized_copy(self):
        """
        makes recognized copy of pdf near specified pdf;

        estimated time: 90s per 400-pages book
        """

        str_path_to_pdf_without_text_layer = r""  # paste path to your pdf to process test
        path_to_pdf_without_text_layer = Path(str_path_to_pdf_without_text_layer)
        if not path_to_pdf_without_text_layer.exists() or len(str_path_to_pdf_without_text_layer) == 0:
            self.assertIs(True, False, "You should specify path to pdf without text layer")
        path_to_result = Path(path_to_pdf_without_text_layer.parent, "ocr_result.pdf")
        Preprocessor._make_recognized_copy(path_to_pdf_without_text_layer, path_to_result, "rus")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
