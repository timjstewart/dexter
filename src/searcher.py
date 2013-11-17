from whoosh.qparser import QueryParser

class Searcher(object):
    def __init__(self, index):
        self._index = index

    def find_by_title(self, title, limit=None):
        with self._index.get_searcher() as s:
            return s.search(self._get_title_query(title), 
                            limit=limit)

    def _get_title_query(self, title):
        parser = self._index.get_query_parser('title')
        return parser.parse(title)

    def find_by_full_text(self, text, limit=None):
        with self._index.get_searcher() as s:
            return s.search(self._get_full_text_query(text), 
                            limit=limit)

    def _get_full_text_query(self, text):
        parser = self._index.get_query_parser('text')
        return parser.parse(text)