import sys
import json
import os
import os.path
import datetime
import bs4

import whoosh.index
from   whoosh.fields import *
from   whoosh.qparser import QueryParser

class IndexWriter(object):
    def __init__(self, writer):
        self._writer = writer

    def add_document(self, path, title, last_modified, text):
        self._writer.update_document(
            last_modified = last_modified,
            title = title,
            path = path,
            text = text)

    def commit(self):
        self._writer.commit()

class Index(object):
    def __init__(self, index_directory, windex):
        self.index_directory = index_directory
        self._index = windex
        self._writer = None

    @staticmethod
    def open_or_create(index_directory):
        if Index.exists(index_directory):
            windex = whoosh.index.open_dir(index_directory)
            return Index(index_directory, windex)
        else:
            if not os.path.isdir(index_directory):
                os.mkdir(index_directory)
            return Index.create(index_directory)

    @staticmethod
    def create(index_directory):
        windex = whoosh.index.create_in(index_directory, 
                                        Index._get_schema())
        return Index(index_directory, windex)

    @staticmethod
    def exists(index_directory):
        return whoosh.index.exists_in(index_directory)

    def get_writer(self):
        return IndexWriter(self._index.writer())

    def get_query_parser(self, field):
        return QueryParser(field, schema=Index._get_schema())

    def get_searcher(self):
        return self._index.searcher()

    def doc_count(self):
        return self._index.doc_count()

    @staticmethod
    def _get_schema():
        return Schema(
            path          = ID(unique=True, stored=True),
            last_modified = STORED,
            title         = TEXT(stored=True),
            text          = TEXT)
