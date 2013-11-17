import os.path

class TextExtractor(object):
    def __init__(self, name, file_name = None):
        self.name = name
        self.file_name = file_name
    def get_title(self):
        pass
    def get_full_text(self):
        pass
    @staticmethod
    def get_extension(file_name):
        return os.path.splitext(file_name)[1]

