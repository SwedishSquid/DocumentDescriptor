from infrastructure.saved_state import SavedStateManager, SavedStateSymbols
from pathlib import Path
import logging


class PreviousProjectsStorageManager:
    """manages storage of paths to previously opened projects"""

    _paths_list_name = 'paths'

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.max_elements_limit = 20
        pass

    def load_projects_paths(self):
        """returns list (might be empty) of Path objects"""
        try:
            data = SavedStateManager.get(
                SavedStateSymbols.LastOpenedProjectsObj)
            paths_strs = data[self._paths_list_name]
            result_paths = []
            for p_str in paths_strs:
                try:
                    result_paths.append(Path(p_str))
                except Exception as e:
                    self.logger.debug(f'seems like cant parse path = {p_str}')
                    self.logger.debug(e)
            return result_paths
        except Exception as e:
            self.logger.exception(e)
            return []
        pass

    def update_projects_list(self, path_to_place_on_top: Path):
        try:
            cur_list = self.load_projects_paths()
            new_list = [str(path_to_place_on_top)]
            for i in range(min(len(cur_list), self.max_elements_limit)):
                path = cur_list[i]
                if path == path_to_place_on_top:
                    continue
                new_list.append(str(path))
            data = {self._paths_list_name: new_list}
            SavedStateManager.put(SavedStateSymbols.LastOpenedProjectsObj, data)
        except Exception as e:
            self.logger.exception(e)
        pass
