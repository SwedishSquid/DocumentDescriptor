import sys
from app.preprocessor_cli import PreprocessorCLI

if __name__ == '__main__':
    PreprocessorCLI().run(['prep', '-p', r'E:\ProjectLib\result_root', 'start'])#sys.argv)
