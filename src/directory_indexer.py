import sys
import json
import os.path
import datetime

from text_extractor_factory import TextExtractorFactory

class DirectoryIndexer(object):
    def __init__(self, index):
        self._index = index
        self._writer = self._index.get_writer()
        self._factory = TextExtractorFactory()

    def index_directory(self, directory):
        os.path.walk(directory, self._index_directory_helper, self)
        self._writer.commit()

    def _index_directory_helper(a, self, directory, names):
        for name in names:
            path = os.path.join(directory, name)
            if self._should_index(path):
                self._index_file(path)

    def _index_file(self, path):
        with open(path, 'r') as f:
            text = f.read()
            extractor = self._factory.get_extractor(text, path)
            if extractor:
                last_modified = os.path.getmtime(path)
                self._writer.add_document(
                    last_modified = last_modified,
                    path = unicode(path, errors='ignore'),
                    title = extractor.get_title(),
                    text = extractor.get_full_text())

    def _should_index(self, path):
        return os.path.isfile(path)

#    def _get_relative_path(self, path):
#        return _u(path[len(self.files_directory):])
