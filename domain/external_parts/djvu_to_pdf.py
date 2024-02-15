from pathlib import Path
import subprocess
import platform


def convert_djvu_to_pdf(src: Path, dst: Path):
    # todo: find a way around for this to work everywhere
    if platform.system().lower() != 'linux':
        raise EnvironmentError(f'conversion not possible on {platform.system()}')
    djvu_path = src
    pdf_path = dst
    command = f'ddjvu -format=pdf "{djvu_path}" "{pdf_path}"'
    res = subprocess.run(command, shell=True)
    if res.returncode != 0:
        # todo: handle this situation somehow
        raise ChildProcessError(f'djvu to pdf conversion not successful; return code {res.returncode}; output = {res.stdout}')
    pass
