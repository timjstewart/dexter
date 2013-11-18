import sys
import json
import datetime
from   flask import Flask, render_template, request
from   werkzeug.wsgi import SharedDataMiddleware
from   index import Index
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
    if query:
        searcher = Searcher(index)
        results = searcher.find_by_full_text(query)
        return render_template("index.html", results=results)
    else:
        return render_template("index.html", 
                               message="Please enter some text")

app.run(debug=True)
