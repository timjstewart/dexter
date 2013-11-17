from index import Index
from directory_indexer import DirectoryIndexer
from searcher import Searcher

def test_documents_found_by_title():
    idx = Index.create('./test_index')
    indexer = DirectoryIndexer(idx)
    indexer.index_directory('./tests/sample_files')
    searcher = Searcher(idx)
    assert 1 == len(searcher.find_by_title(u'one'))

def test_documents_found_by_full_text():
    idx = Index.create('./test_index')
    indexer = DirectoryIndexer(idx)
    indexer.index_directory('./tests/sample_files')
    searcher = Searcher(idx)
    assert 2 == len(searcher.find_by_full_text(u'Funny'))
