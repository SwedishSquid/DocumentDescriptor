from domain.engine import Engine
from domain.book_data_holders.book_meta import BookMeta
from domain.book_data_holders.book_info import BookInfo
from domain.book_data_holders.description_stage import DescriptionStage
from domain.glue import Glue


# todo: rename file??
class App:
    def __init__(self):
        self.engine: Engine = None
        self.glue: Glue = None
        pass

    def reset_engine(self):
        self.engine = self.glue.get_engine()

    def try_set_project_path(self, project_path):
        self.glue = Glue(project_path)
        if not self.glue.init_happened():
            return False
        self.engine = self.glue.get_engine()
        return True

    def get_next_book(self):
        """change current book to current next book
        (increment index + return book_info)"""
        if not self.engine.try_set_book_index(self.engine.current_book_index + 1):
            return None
        return self.get_current_book()

    def get_current_book(self):
        # todo: make something with zero book problem
        book_info = self.engine.get_current_book()
        return book_info

    def try_set_index_and_get_book(self, index: int):
        #
        if not self.engine.try_set_book_index(index):
            return False
        return self.get_current_book()

    def get_book_number(self, book_info: BookInfo):
        # todo: implement this method
        return ''

    def get_book_description_stage(self, book_info: BookInfo):
        # todo: implement this method
        return DescriptionStage.NOT_STARTED

    def save_as_rejected(self, meta: BookMeta, message=''):
        """:param message: text explaining why this book is rejected"""
        # todo: save this message somewhere
        self.engine.save_book_data(meta, DescriptionStage.REJECTED, message)
        pass

    def save_as_finished(self, meta: BookMeta):
        self.engine.save_book_data(meta, DescriptionStage.FINISHED)
        pass

    def save_as_in_progress(self, meta: BookMeta):
        self.engine.save_book_data(meta, DescriptionStage.IN_PROGRESS)

    def save_with_previous_state_flag(self, meta: BookMeta):
        """if previous state is NOT_STARTED,
         then new state will be IN_PROGRESS
        """
        cur_state = self.get_current_book().description_stage
        if cur_state == DescriptionStage.NOT_STARTED:
            cur_state = DescriptionStage.IN_PROGRESS
        self.engine.save_book_data(meta, cur_state)
        pass

    def get_full_book_list(self):
        return self.engine.get_full_book_list()

    pass
