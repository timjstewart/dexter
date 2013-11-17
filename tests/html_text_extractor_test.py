from html_text_extractor import HtmlTextExtractor

def test_title_extraction():
    text = "<html><head><title>Hello</title></head></html>"
    assert "Hello" == HtmlTextExtractor(text).get_title()

def test_title_extraction_with_no_title():
    text = "<html><head></head></html>"
    assert "" == HtmlTextExtractor(text).get_title()

def test_can_analyze_html():
    assert HtmlTextExtractor.can_analyze("foo.html")

def test_can_analyze_htm():
    assert HtmlTextExtractor.can_analyze("foo.htm")
