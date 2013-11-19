import os
import pickle

_DOC_SET_FILE_NAME = 'docset.pickle'

class DocSet(object):
    def __init__(self, index_directory):
        self._index_directory = index_directory

    def get_doc_set_names(self):
        path = self._get_doc_set_file_path()
        if os.path.isfile(path):
            with open(path, 'r') as f:
                return pickle.load(f)
        else:
            return set()

    def add_doc_set(self, name):
        p = self.get_doc_set_names()
        p.add(name)
        path = self._get_doc_set_file_path()
        with open(path, 'w') as f:
            pickle.dump(p, f)
        
    def _get_doc_set_file_path(self):
        return os.path.join(self._index_directory, _DOC_SET_FILE_NAME)
