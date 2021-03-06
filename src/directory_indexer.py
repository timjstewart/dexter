import sys
import json
import copy
import os.path
from   datetime import datetime

from text_extractor_factory import TextExtractorFactory
from searcher import Searcher

class DirectoryIndexer(object):
    def __init__(self, index):
        self._index = index
        self._writer = None
        self._factory = TextExtractorFactory()

    def index_directory(self, directory):
        self._writer = self._index.get_writer()
        os.path.walk(directory, self._index_directory_helper, self)
        self._writer.commit()
        self._writer = None

    @staticmethod
    def _index_directory_helper(self, directory, names):
        print "Indexing %s..." % directory
        for name in names:
            path = os.path.join(directory, name)
            if self._should_index(path):
                self._index_file(path)

    def _index_file(self, path):
        with open(path, 'r') as f:
            text = f.read()
        extractor = self._factory.get_extractor(text, path)
        if extractor:
            title = extractor.get_title()
            full_text = extractor.get_full_text()
            if title and full_text:
                print("Indexing: %s" % path)
                self._writer.update_document(**self.get_fields(
                    path, title, full_text
                ))

    def get_fields(self, path, title, full_text):
        return {
            'last_modified': os.path.getmtime(path),
            'path': unicode(path, errors='ignore'),
            'title': title,
            'text':  full_text
        }

    def _should_index(self, path):
        return (os.path.isfile(path) and
                not self._is_indexed_file_current(path))

    def _is_indexed_file_current(self, path):
        results = Searcher(self._index).find_by_path(unicode(path))
        if results and len(results) >= 1:
            last_modified = datetime.fromtimestamp(os.path.getmtime(path))
            last_indexed  = results[0].last_modified
            return last_modified <= last_indexed
        else:
            return False
        
        
