import sys
import json

from flask import Flask, render_template, request
from index import Index
from searcher import Searcher

app = Flask("dexter")

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/search/title")
def search():
    global index
    query = request.args.get('q')
    searcher = Searcher(index)
    results = searcher.find_by_title(query)
    return _format_results(results)

def _format_results(results):        
    hits = []
    for result in results:
        hits.append({
            'path': result.path,
            'last_modified': result.last_modified
        })
    return json.dumps(hits)

def run_server(index_directory):
    app.run(debug=True)

def usage():
    print("usage: python dexter.py INDEX_DIR")
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        global index
        index = Index.open_or_create(sys.argv[1])
        run_server(sys.argv[1])
    else:
        usage()

