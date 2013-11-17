from text_extractor import TextExtractor
from bs4 import BeautifulSoup
import datetime

class HtmlTextExtractor(TextExtractor):
    def __init__(self, text, file_name = None):
        super(HtmlTextExtractor, self).__init__("HTML", file_name)
        self._soup = None
        self._text = text
    @staticmethod
    def can_analyze(file_name):
        ext = TextExtractor.get_extension(file_name) 
        return ext.lower() in [ '.html', '.htm' ]
    def get_title(self):
        title = self._get_soup().title
        if title:
            return title.string.strip()
        else:
            return unicode('')
    def get_full_text(self):
        return self._get_soup().get_text().strip()
    def _get_soup(self):
        if not self._soup:
            self._soup = BeautifulSoup(self._text)
        return self._soup
