import utils
from pathlib import Path
import logging


class SavedStateManager:
    """singleton for saving user specific information;
     like font size or last opened project"""
    RelFilePath = 'temp/saved_state.json'

    @classmethod
    def get(cls, name: str, default_value=None):
        """might be i/o bound - reading from/writing to file
           :param name: name of the object you want to retrieve
           :param default_value: value to return if nothing found
           """
        logger = logging.getLogger(__name__)
        try:
            data = cls._fetch_data()
            return data[name]
        except IndexError as e:
            logger.debug(f'value named {name} not found in saved; return default')
            return default_value
        except Exception as e:
            logger.error(e)
            return default_value
        pass

    @classmethod
    def put(cls, name: str, value):
        """might be i/o bound - reading from/writing to file
           :param name: name of the object to save
           :param value: value to save (works with strings, nums, true / false / none)
        """
        try:
            data = cls._fetch_data()
            data[name] = value
            cls._save_data(data)
        except Exception as e:
            logging.getLogger(__name__).error(e)
        pass

    @classmethod
    def _get_filepath(cls):
        return Path(utils.get_app_root_path(), cls.RelFilePath)

    @classmethod
    def _fetch_data(cls):
        try:
            with open(cls._get_filepath(), encoding='utf-8') as f:
                data = utils.json_loads(f.read())
            return data
        except Exception as e:
            logging.getLogger(__name__).error(e)
            return {}
        pass

    @classmethod
    def _save_data(cls, data):
        try:
            utils.make_directory(cls._get_filepath().parent,
                                 parents=True, exist_ok=True)
            with open(cls._get_filepath(), encoding='utf-8', mode='w+') as f:
                f.write(utils.json_dumps(data))
        except Exception as e:
            logging.getLogger(__name__).error(e)
        pass
    pass


class SavedStateSymbols:
    FontSize = 'font_size'
    LastOpenedProjectsObj = 'last_opened_projects_obj'
