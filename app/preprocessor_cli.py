import argparse
from pathlib import Path
from domain.submodules.project_folder_manager import ProjectFolderManager
from domain.preprocessor import Preprocessor
from UI.console_progress_bar import printProgressBar


class PreprocessorCLI:
    """console interface for preprocessing"""
    _version = '0.1.0'      # todo: store version somewhere else
    _verbosity_level = 1

    def run(self, arguments):
        parser = self._get_parser()
        args = parser.parse_args(arguments[1:])
        self._verbosity_level = args.verbose
        args.func(args)
        pass

    def start_handler(self, args):
        if Preprocessor.is_preprocessed(args.project):
            self.output('it seems that preprocessing already took place', verbosity=0)
            return
        self.output('attempt to preprocess')
        ProjectFolderManager.check_project_consistency(args.project)
        for done, total in Preprocessor(project_dir=args.project).preprocess_with_generator():
            if self._verbosity_level >= 1:
                printProgressBar(done, total, prefix='Progress', suffix=f'Complete | {done}/{total}', length=50)
        self.output('done')
        pass

    def init_handler(self, args):
        self.output('attempt to initialize the project')
        results = ProjectFolderManager.init_project(project_folder=args.project)
        for res in results:
            self.output(res)
        pass

    def _get_parser(self):
        parser = argparse.ArgumentParser(prog='preprocessor',
                                         epilog='source: https://github.com/SwedishSquid/DocumentDescriptor')
        parser.add_argument('--version', action='version',
                            version=f'%(prog)s {self._version}',
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


# PreprocessorCLI().run(sys.argv)
