from pathlib import Path
import subprocess
import platform
import logging

import utils


class OCRError(Exception):
    """raised when something wrong with ORC"""
    pass


class Recognizer:
    # ocrmypdf ./source/big_rus.pdf ./big_rus_ocr.pdf -l rus+eng --pages 1-5 --clean  -q
    @staticmethod
    def ocr(src_path: Path, dst_path: Path, language_arg: str, pages_arg: str,
            subp_output_file=None):
        logger = logging.getLogger(__name__)
        logger.info('OCR method called')
        if platform.system().lower() != 'linux':
            message = 'OCR is currently supported on linux systems only; very likely that programm won`t be able to perform OCR'
            logger.warning(message)
        src = str(src_path)
        dst = str(dst_path)
        language = f'-l {language_arg}'
        if pages_arg is None:
            pages = ''
        else:
            pages = f'--pages {pages_arg}'
        command = f'ocrmypdf "{src}" "{dst}" {language} {pages} --clean -q'
        logger.info(f'OCR subprocess command >> {command}')
        # todo: check if this file is ok
        if subp_output_file is None:
            completed_process = subprocess.run(command, shell=True)
        else:
            with open(subp_output_file, 'w') as file:
                completed_process = subprocess.run(command, shell=True, stdout=file)
        logger.info(f'subprocess return code = {completed_process.returncode}')
        try:
            completed_process.check_returncode()
        except subprocess.CalledProcessError as e:
            logger.debug(f'OCR failed with {e.with_traceback(tb=None)}')
            raise OCRError(e)
        pass
    pass
