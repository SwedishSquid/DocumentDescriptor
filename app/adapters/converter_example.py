import subprocess
import os

djvu_file_path = r'/home/me/dev/djvu_to_pdf/book.djvu'
pdf_file_path = r'/home/me/dev/djvu_to_pdf/book.pdf'


def convert(djvu_abs_path, pdf_abs_path):
    command = f'ddjvu -format=pdf {djvu_abs_path} {pdf_abs_path}'
    res = subprocess.run(command, shell=True)
    print(res)
    pass

convert(djvu_file_path, pdf_file_path)