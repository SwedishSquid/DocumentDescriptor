import logging
from pathlib import Path
import utils


def configure_main_logger(level='INFO'):
    logger = logging.getLogger('root')
    logger.setLevel(level)

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
    return logger


# configure_logger('root')
# logging.warning('jsdhfkjshfkjshdfkjhsk vjseiufh')
