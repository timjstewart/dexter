import sys
import json
import datetime
from   flask import Flask, render_template, request
from   werkzeug.wsgi import SharedDataMiddleware
from   index import Index
from   doc_set import DocSet
from   searcher import Searcher
from   jinja2 import Markup

def usage():
    print("usage: python dexter.py FILES_DIR INDEX_DIR")
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        files_root_directory = sys.argv[1]
        index_directory = sys.argv[2]
        index = Index.open_or_create(index_directory)
        app = Flask("dexter")
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/content' : '/' # files_root_directory
        })
    else:
        usage()

@app.route("/")
def root():
    return render_template("index.html", results=[])

@app.route("/search")
def search():
    global index
    query = request.args.get('q')
    doc_set = request.args.get('d')
    doc_set_names = DocSet(index_directory).get_doc_set_names()
    if query:
        if doc_set != 'all':
            actual_query = u"text:%s doc_set:%s" % (
                query, doc_set)
        else:
            actual_query = query
        searcher = Searcher(index)
        results = searcher.find_by_full_text(actual_query)
        return render_template("index.html", 
                               results=results, 
                               query = query,
                               selected_doc_set = doc_set,
                               doc_set_names = doc_set_names)
    else:
        return render_template("index.html", 
                               message = "Please enter some text",
                               doc_set_names = doc_set_names)

app.run(debug=True)
