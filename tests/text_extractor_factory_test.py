from text_extractor_factory import TextExtractorFactory

def test_create_html_text_extractor():
    html = '<html><head><title>Hello</title></head></html>'
    extractor = TextExtractorFactory().get_extractor(html, 'greeting.htm')
    assert extractor.name == 'HTML'

def test_create_png_text_extractor():
    extractor = TextExtractorFactory().get_extractor(None, 'greeting.png')
    assert extractor == None
