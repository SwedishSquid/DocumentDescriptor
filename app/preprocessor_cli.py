import argparse
from pathlib import Path
from UI.console_progress_bar import printProgressBar
from domain.glue import Glue
import version


class PreprocessorCLI:
    """console interface for preprocessing"""
    _verbosity_level = 1

    def run(self, arguments):
        parser = self._get_parser()
        args = parser.parse_args(arguments[1:])
        self._verbosity_level = args.verbose
        args.func(args)
        pass

    def start_handler(self, args):
        self.output('attempt to preprocess')
        glue = Glue(args.project)
        ms_receiver = lambda s: self.output(s)
        if not glue.init_happened(ms_receiver=ms_receiver):
            self.output(f'folder {args.project} not recognized as a project')
            return

        generator, total_book_count = glue.get_preprocessor_generator(ms_receiver=ms_receiver)
        completed_count = 0
        skipped_count = 0
        self._print_progress_bar(completed_count, total_book_count)
        for completed_book_preprocessing in generator:
            completed_count += 1
            if completed_book_preprocessing.success:
                self._print_progress_bar(completed_count, total_book_count)
            else:
                skipped_count += 1
                self.output(f'can`t preprocess {completed_book_preprocessing.original_book_path}')
                if glue.get_project_manager(self.output).config.stop_when_cant_preprocess:
                    self.output('stop preprocessing cause cannot preprocess')
                    break
        self.output(f'preprocessed {completed_count - skipped_count}')
        pass

    def init_handler(self, args):
        self.output('attempt to initialize the project')
        Glue(args.project).init_project(ms_receiver=lambda s: self.output(s))
        pass

    def _print_progress_bar(self, completed_count, total_count):
        suffix = f'Complete | {completed_count}/{total_count}'
        printProgressBar(completed_count, total_count,
                         prefix='Progress', suffix=suffix, length=50)
        pass

    def _get_parser(self):
        parser = argparse.ArgumentParser(prog='preprocessor',
                                         epilog='source: https://github.com/SwedishSquid/DocumentDescriptor')
        parser.add_argument('--version', action='version',
                            version=f'%(prog)s {version.get_version()}',
                            help='current version')
        parser.add_argument('-v', '--verbose',
                            type=int,
                            help='verbosity level; defaults to 1',
                            default=1,
                            choices=[0, 1, 2])
        parser.add_argument('-p', '--project',
                                  type=Path,
                                  default=Path.cwd(),
                                  help='path to project directory')

        subparsers = parser.add_subparsers(required=True)

        start_parser = subparsers.add_parser('start',
                                             help='start preprocessing')

        start_parser.set_defaults(func=self.start_handler)

        init_parser = subparsers.add_parser('init',
                                            help='add default project files in selected directory')
        init_parser.set_defaults(func=self.init_handler)

        return parser

    def output(self, data, end=None, verbosity=1):
        if self._verbosity_level >= verbosity:
            print(data, end=end)
        pass
    pass
