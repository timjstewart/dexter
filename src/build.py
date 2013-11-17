import sys
from   index import Index
from   directory_indexer import DirectoryIndexer 

def usage():
    print("usage: python build.py FILES_DIR INDEX_DIR")
    sys.exit(0)

def build_index(files_dir, index_dir):
    idx = Index.open_or_create(index_dir)
    idxer = DirectoryIndexer(idx)
    idxer.index_directory(files_dir)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        files_dir = sys.argv[1]
        index_dir = sys.argv[2]
        build_index(files_dir, index_dir)
    else:
        usage()
