import logging
from pathlib import Path
import utils
import sys
import traceback


default_log_level = 'WARNING'


def _load_possible_log_level():
    filepath = Path(utils.get_app_root_path(), 'app-logs', 'log-config.json')
    saved_level = None
    possible_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if utils.is_file(filepath):
        try:
            saved_level = utils.json_loads(utils.read_text_from_file(filepath))['log_level']
        except Exception:
            # todo: handle better
            saved_level = None
        pass

    if saved_level not in possible_levels:
        default_log_config = {
            'comment_on_log_levels': 'possible variants: DEBUG, INFO, WARNING, ERROR, CRITICAL; DEBUG is most informative, CRITICAL is the least; see python logging module for more info',
            'log_level': default_log_level
        }
        utils.make_directory(filepath.parent, parents=True, exist_ok=True)
        utils.write_text_to_file(filepath, utils.json_dumps(default_log_config))
        return default_log_level
    return saved_level


def _set_logging_level(logger, level=None):
    if level is None:
        level = _load_possible_log_level()
    logger.setLevel(level)
    pass


def _set_exception_hook():
    def my_exception_hook(type, value, tb):
        logging.critical(f'something happened again, uncaught exception of type = {type}, value = {value}')
        logging.critical(f'traceback = {traceback.extract_tb(tb)}')
        raise type(value)   # reraise exception
        pass
    sys.excepthook = my_exception_hook
    pass


def configure_main_logger(level=None):
    logger = logging.getLogger('root')

    _set_logging_level(logger, level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    path = Path(utils.get_app_root_path(), 'app-logs', 'main.log')
    if not path.exists():
        path.parent.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(filename=path, mode='w', encoding='utf-8', )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _set_exception_hook()
    return logger





# configure_logger('root')
# logging.warning('jsdhfkjshfkjshdfkjhsk vjseiufh')
