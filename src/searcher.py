from whoosh.qparser import QueryParser
from datetime import datetime
from bs4 import BeautifulSoup
from text_extractor_factory import TextExtractorFactory

class SearchHit(object):
    def __init__(self, hit):
        self.title = hit['title']
        self.path = hit['path']
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

    def _get_title_query(self, title):
        parser = self._index.get_query_parser('title')
        return parser.parse(title)


    def _get_full_text_query(self, text):
        parser = self._index.get_query_parser('text')
        return parser.parse(text)
