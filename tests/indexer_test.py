from index import Index
from directory_indexer import DirectoryIndexer

def test_documents_added():
    idx = Index.create('./test_index')
    indexer = DirectoryIndexer(idx)
    indexer.index_directory('./tests/sample_files')
    assert idx.doc_count() == 3
