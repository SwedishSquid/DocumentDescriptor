from pathlib import Path
import subprocess
import platform


class Recognizer:
    # ocrmypdf ./source/big_rus.pdf ./big_rus_ocr.pdf -l rus+eng --pages 1-5 --clean  -q
    @staticmethod
    def ocr(src_path: Path, dst_path: Path, language_arg: str, pages_arg: str):
        if platform.system().lower() != 'linux':
            raise EnvironmentError(f'ocr on your platform({platform.system()}) not supported')

        src = str(src_path)
        dst = str(dst_path)
        language = f'-l {language_arg}'
        if pages_arg is None:
            pages = ''
        else:
            pages = f'--pages {pages_arg}'
        command = f'ocrmypdf "{src}" "{dst}" {language} {pages} --clean -q'
        res = subprocess.run(command, shell=True)
        # todo: handle return code != 0
        # check lang errors
        pass
    pass
