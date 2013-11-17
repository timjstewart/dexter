import sys
import json

from flask import Flask, render_template, request
from index import Index

from werkzeug.wsgi import SharedDataMiddleware

from searcher import Searcher

def usage():
    print("usage: python dexter.py INDEX_DIR")
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        index_directory = sys.argv[1]
        files_root_directory = sys.argv[2]

        index = Index.open_or_create(index_directory)
        app = Flask("dexter")
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/content' : '/' # files_root_directory
        })
    else:
        usage()

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/search/title")
def search_title():
    global index
    query = request.args.get('q')
    searcher = Searcher(index)
    results = searcher.find_by_title(query)
    return _format_results(results)

@app.route("/search/text")
def search_text():
    global index
    query = request.args.get('q')
    searcher = Searcher(index)
    results = searcher.find_by_full_text(query)
    return _format_results(results)

def _format_results(results):        
    hits = []
    for result in results:
        hits.append({
            'title': result.title,
            'path': result.path,
            'last_modified': result.last_modified
        })
    return json.dumps(hits)


app.run(debug=True)
