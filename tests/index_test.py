from index import Index

def test_index_does_not_exist():
    assert not Index.exists('wrong')

def test_index_exists():
    dir = './test_index'
    Index.create(dir)
    assert Index.exists(dir)

def test_new_index_has_zero_documents():
    dir = './test_index'
    idx = Index.create(dir)
    assert idx.doc_count() == 0

def test_index_file():
    dir = './test_index'
    idx = Index.create(dir)
    writer = idx.get_writer()
    writer.add_document(
        path = u'/foo/bar',
        title = u'Foo: The History',
        last_modified = 34343423423,
        text = u'Not much to say here')
    writer.commit()
    assert idx.doc_count() == 1

