from pathlib import Path
import subprocess
import platform

import utils


def convert_djvu_to_pdf(src: Path, dst: Path, stderr_filepath: Path=None):
    # todo: find a way around for this to work everywhere
    if platform.system().lower() != 'linux':
        raise EnvironmentError(f'conversion not possible on {platform.system()}')
    djvu_path = src
    pdf_path = dst
    command = f'ddjvu -format=pdf "{djvu_path}" "{pdf_path}"'
    # todo: check if this file is ok
    if stderr_filepath is not None:
        with open(stderr_filepath, 'w') as file:
            res = subprocess.run(command, shell=True, stderr=file)
    else:
        res = subprocess.run(command, shell=True)
    if res.returncode != 0:
        # todo: handle this situation somehow
        raise ChildProcessError(f'djvu to pdf conversion not successful; return code {res.returncode}; output = {res.stdout}')
    pass
