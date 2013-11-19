from whoosh.qparser import QueryParser
from datetime import datetime
from bs4 import BeautifulSoup
from text_extractor_factory import TextExtractorFactory

class SearchHit(object):
    def __init__(self, hit):
        self.title = hit['title']
        self.path = hit['path']
        self.doc_set = hit['doc_set']
        self.last_modified = datetime.fromtimestamp(hit['last_modified'])
        with open(self.path, 'r') as f:
            self.highlights = self._get_highlights(hit)

    def _get_highlights(self, hit):
        with open(self.path, 'r') as f:
            text = unicode(f.read(), errors='ignore')
            factory = TextExtractorFactory()
            extractor = factory.get_extractor(text, hit['path'])
            return hit.highlights('text', text=extractor.get_full_text())

class Searcher(object):
    def __init__(self, index):
        self._index = index

    def find_by_path(self, path, limit=1):
        with self._index.get_searcher() as s:
            return [SearchHit(hit) for hit 
                    in s.search(self._get_path_query(path), 
                                limit=limit)]

    def find_by_title(self, title, limit=20):
        with self._index.get_searcher() as s:
            return [SearchHit(hit) for hit 
                    in s.search(self._get_title_query(title), 
                                limit=limit)]

    def find_by_full_text(self, text, limit=20):
        with self._index.get_searcher() as s:
            return [SearchHit(hit) for hit 
                    in s.search(self._get_full_text_query(text), 
                                limit=limit)]

    def _parse_field_query(self, field_name, query_text):
        parser = self._index.get_query_parser(field_name)
        return parser.parse(query_text)

    def _get_path_query(self, path):
        return self._parse_field_query('path', path)

    def _get_title_query(self, title):
        return self._parse_field_query('title', title)

    def _get_full_text_query(self, text):
        return self._parse_field_query('text', text)


