import subprocess
import platform
from pathlib import Path
from domain.book_data_holders.book_info import BookInfo


class DjvuPdfConverter:
    buffer_local_path = 'temp/buffer_book.pdf'

    def __init__(self, project_path):
        self.buffer_abs_path = Path(project_path, self.buffer_local_path)
        pass

    def try_replace_djvu_book_with_pdf_clone(self, book_info: BookInfo):
        print('replacement called')
        if book_info.absolute_path.suffix != '.djvu':
            print('suffix incorrect')
            return False
        if not self.check_platform():
            print(f'platform {platform.system()} not supported')
            return False
        success = self._try_convert(book_info.absolute_path, self.buffer_abs_path)
        if success:
            book_info.absolute_path = self.buffer_abs_path
        return success

    @staticmethod
    def check_platform():
        return platform.system().lower() == 'linux'

    def _try_convert(self, djvu_abs_path, pdf_abs_path):
        print('conversion attempt')
        command = f'ddjvu -format=pdf "{djvu_abs_path}" "{pdf_abs_path}"'
        res = subprocess.run(command, shell=True)
        print(res)
        print(f'status = {res.returncode}')
        return res.returncode == 0
    pass
