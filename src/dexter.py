import sys
import json
import os.path
import datetime

from flask import Flask, render_template, request
import whoosh.index
from whoosh.fields import *
from whoosh.qparser import QueryParser

app = Flask("dexter")
search_ix=None
document_root=None

def get_schema():
    return Schema(
        path       = ID(unique=True, stored=True),
        indexed_at = STORED,
        content    = TEXT)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/search/<q>")
def search(q):
    try:
        with search_ix.searcher() as searcher:
            query = QueryParser("content", search_ix.schema).parse(q)
            results = searcher.search(query)
            hits = []
            for result in results:
                hits.append({
                    'path': result.fields()['path'],
                    'indexed_at': result.fields()['indexed_at']
                })
            return json.dumps(hits)
    except Exception, ex:
        return "EX: " + ex.message

def find_document_by_path(path):
    with search_ix.searcher() as searcher:
        query = QueryParser("indexed_at", search_ix.schema).parse(path)
        results = searcher.search(query)
        if len(results) == 0:
            return None
        elif len(results) >= 1:
            return results[0]

def create_index(index_directory):
    return whoosh.index.create_in(
        index_directory, get_schema())

def open_index(index_directory):
    if whoosh.index.exists_in(index_directory):
        print "opening existing index"
        return whoosh.index.open_dir(index_directory)
    else:
        print "creating index"
        return create_index(index_directory)

def run_server(index_directory, doc_directory):
    global search_ix
    global document_root
    document_root = doc_directory
    search_ix = open_index(index_directory)
    app.run(debug=True)

def index_file(writer, file_name, rel_path):
    with open(file_name) as f:
        contents = f.read()
        try:
            modtime = os.path.getmtime(file_name)
            print("Indexing %s" % file_name)
            writer.update_document(
                indexed_at = modtime,
                path = unicode(rel_path, errors = 'ignore'),
                content = unicode(contents, errors='ignore'))
        except Exception, ex:
            print("Can't index: %s.  Error: %s" % (
                file_name, ex))

def should_index(file_name, rel_path):
    print(find_document_by_path(rel_path))
    return os.path.isfile(file_name)

def index_directory((root_directory,writer), directory, names):
    for name in names:
        file_name = os.path.join(directory, name)
        rel_path  = os.path.join(directory[len(root_directory):], name)
        if should_index(file_name, rel_path):
            index_file(writer, file_name, rel_path)

def index(index_dir, directory):
    global search_ix
    search_ix = open_index(index_dir)
    writer = search_ix.writer()
    os.path.walk(directory, index_directory, (directory, writer))
    writer.commit()

def usage():
    print("usage: python dexter.py COMMAND ARGS")
    print("COMMAND:")
    print("  server INDEX_DIR")
    print("  index INDEX_DIR FILES_DIR")
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == 'index':
        index(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 4 and sys.argv[1] == 'server':
        run_server(sys.argv[2], sys.argv[3])
    else:
        usage()

