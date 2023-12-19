import subprocess
import platform
from pathlib import Path
from domain.book_data_holders.book_info import BookInfo


djvu_file_path = r'/home/me/dev/djvu_to_pdf/book.djvu'
pdf_file_path = r'/home/me/dev/djvu_to_pdf/book.pdf'


class DjvuPdfConverter:
    buffer_local_path = 'temp/buffer_book.pdf'

    def __init__(self, project_path):
        self.buffer_abs_path = Path(project_path, self.buffer_local_path)
        pass

    def try_replace_djvu_book_with_pdf_clone(self, book_info: BookInfo):
        if str(book_info.absolute_path)[-5:] != '.djvu':
            return False
        if not self.check_platform():
            return False
        success = self.try_convert(book_info.absolute_path, self.buffer_abs_path)
        if success:
            book_info.absolute_path = self.buffer_abs_path
        return success

    def check_platform(self):
        return platform.system().lower() == 'linux'

    def try_convert(self, djvu_abs_path, pdf_abs_path):
        command = f'ddjvu -format=pdf {djvu_abs_path} {pdf_abs_path}'
        res = subprocess.run(command, shell=True)
        return res.returncode == 0
    pass


# convert(djvu_file_path, pdf_file_path)
