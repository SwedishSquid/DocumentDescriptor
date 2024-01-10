import argparse
from pathlib import Path
from UI.console_progress_bar import printProgressBar
from domain.glue import Glue


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
        self.output('attempt to preprocess')
        glue = Glue(args.project)
        ms_receiver = lambda s: self.output(s)
        if not glue.init_happened(ms_receiver=ms_receiver):
            self.output(f'folder {args.project} not recognized as a project')
            return

        for done, total in glue.get_preprocessor_generator(ms_receiver=ms_receiver):
            printProgressBar(done, total, prefix='Progress', suffix=f'Complete | {done}/{total}', length=50)
        self.output('done')
        pass

    def init_handler(self, args):
        self.output('attempt to initialize the project')
        Glue(args.project).init_project(ms_receiver=lambda s: self.output(s))
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
