import os
from   whoosh.fields import *
from   index import Index
from   directory_indexer import DirectoryIndexer
from   doc_set import DocSet

_DOC_SET_FIELD = 'doc_set'

class _DocSetIndexer(DirectoryIndexer):
    def __init__(self, index, name):
        super(_DocSetIndexer, self).__init__(index)
        self._name = name

    def get_fields(self, path, title, full_text):
        fields = super(_DocSetIndexer, self).get_fields(
            path, title, full_text)
        fields[_DOC_SET_FIELD] = unicode(self._name, errors='ignore')
        return fields

class LibraryIndexer(object):
    def __init__(self, root_directory, index_directory):
        self._root_directory = root_directory
        self._index_directory = index_directory

    def index_doc_set(self, doc_set_name):
        path = os.path.join(self._root_directory, doc_set_name)
        if os.path.isdir(path):
            idx = Index.open_or_create(self._index_directory)
            doc_set = DocSet(self._index_directory)
            doc_set.add_doc_set(doc_set_name)
            idx.add_field(_DOC_SET_FIELD, TEXT(stored=True))
            idxr = _DocSetIndexer(idx, doc_set_name)
            idxr.index_directory(path)

    def index_library(self):
        for doc_set_name in os.listdir(self._root_directory):
            self.index_doc_set(doc_set_name)
                
