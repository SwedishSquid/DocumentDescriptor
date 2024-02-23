# todo: add reason message? or exception type
class CompletedBookPreprocessing:
    """contains information about one completed book preprocessing;
    if it was successfully completed, and book path"""
    def __init__(self, success: bool, original_book_path):
        self.success = success
        self.original_book_path = original_book_path
        pass
    pass
