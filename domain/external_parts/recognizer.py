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
            subp_output_file=None, other_args=None):
        if other_args is None:
            other_args = ''
        logger = logging.getLogger(__name__)
        logger.info('OCR method called')
        if platform.system().lower() != 'linux':
            message = 'OCR is currently supported on linux systems only; very likely that programm won`t be able to perform OCR'
            logger.warning(message)
        src = str(src_path)
        dst = str(dst_path)
        command = ' '.join([f'ocrmypdf', f'"{src}"', f'"{dst}"', '-l' f'{language_arg}', f'--pages', f'{pages_arg}', '--clean', other_args])  # -q'      # where -q means quiet - no console output
        logger.info(f'OCR subprocess command >> {command}')
        # todo: check if this file is ok
        if subp_output_file is None:
            completed_process = subprocess.run(command, shell=True)
        else:
            with open(subp_output_file, 'w') as file:
                completed_process = subprocess.run(command, stdout=file,
                                                   stderr=subprocess.STDOUT, shell=True)
        logger.info(f'subprocess return code = {completed_process.returncode}')
        try:
            completed_process.check_returncode()
        except subprocess.CalledProcessError as e:
            logger.debug(f'OCR failed with {e}')
            raise OCRError(e)
        pass
    pass
