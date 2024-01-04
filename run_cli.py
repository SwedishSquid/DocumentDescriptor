from pathlib import Path
from domain.cli_test import CLI


if __name__ == "__main__":
    path_to_proj = None # Path(r'E:\ProjectLib\result_root')
    if path_to_proj is None:
        print('insert path to project first')
    else:
        CLI().run(path_to_proj)
