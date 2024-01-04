from domain.book_data_holders.book_meta import BookMeta
from domain.book_data_holders.book_meta_scheme import BookMetaScheme
from domain.book_data_holders.description_stage import DescriptionStage
from pathlib import Path


class BookInfo:
    """yep, another book_thing
    это <<расширенная>> book_meta
    содержит больше информации, чем записывается в файл
    например путь до книги, названия полей на русском, description stage"""

    def __init__(self, book_meta: BookMeta, absolute_path,
                 meta_scheme: BookMetaScheme, descr_stage: DescriptionStage):
        self.book_meta = book_meta
        self.absolute_path = Path(absolute_path)
        self.meta_scheme = meta_scheme
        self._description_stage = descr_stage
        pass

    def get_human_readable_name(self, name: str):
        return self.meta_scheme.get_human_readable_name(name)

    @property
    def description_stage(self):
        return self._description_stage
    pass
