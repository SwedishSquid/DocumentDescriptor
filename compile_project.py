import PyInstaller.__main__


def compile_descriptor_app():
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--name', 'descriptor',
        # '--noconsole'     # leaves only GUI; ignored on linux
    ])


def compile_preprocessor_app():
    PyInstaller.__main__.run([
        'run_preprocessor_cli.py',
        '--onefile',
        '--name', 'preprocessor'
    ])


if __name__ == '__main__':
    compile_descriptor_app()
    compile_preprocessor_app()
