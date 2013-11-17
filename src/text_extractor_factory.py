from html_text_extractor import HtmlTextExtractor

class TextExtractorFactory(object):
    def get_extractor(self, file_contents, file_name):
        if HtmlTextExtractor.can_analyze(file_name):
            return HtmlTextExtractor(file_contents, file_name)
        else:
            return None
