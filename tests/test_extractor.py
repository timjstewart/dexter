from text_extractor import TextExtractor

def test_file_extension():
    assert '.png' == TextExtractor.get_extension('dolphin.png')

def test_file_extension_no_extension():
    assert '' == TextExtractor.get_extension('dolphin')
