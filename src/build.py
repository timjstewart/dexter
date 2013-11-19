import sys
from   index import Index
from   directory_indexer import DirectoryIndexer 
from   library_indexer import LibraryIndexer

def usage():
    print("usage: python build.py FILES_DIR INDEX_DIR")
    sys.exit(0)

def build_index(files_dir, index_dir):
    idxer = LibraryIndexer(files_dir, index_dir)
    idxer.index_library()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        files_dir = sys.argv[1]
        index_dir = sys.argv[2]
        build_index(files_dir, index_dir)
    else:
        usage()
