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

    def update_document(self, **kwargs):
        self._writer.update_document(**kwargs)

    def commit(self):
        self._writer.commit()

class Index(object):
    def __init__(self, index_directory, index):
        self.index_directory = index_directory
        self._index = index
        self._writer = None

    @staticmethod
    def open_or_create(index_directory):
        if Index.exists(index_directory):
            index = whoosh.index.open_dir(index_directory)
            return Index(index_directory, index)
        else:
            if not os.path.isdir(index_directory):
                os.mkdir(index_directory)
            return Index.create(index_directory)

    @staticmethod
    def create(index_directory):
        index = whoosh.index.create_in(index_directory, 
                                        Index._get_schema())
        return Index(index_directory, index)

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
        
    def add_field(self, field_name, field_spec):
        try:
            return self._index.add_field(field_name, field_spec)
        except whoosh.fields.FieldConfigurationError:
            pass

    @staticmethod
    def _get_schema():
        return Schema(
            path          = ID(unique=True, stored=True),
            last_modified = STORED,
            title         = TEXT(stored=True),
            text          = TEXT(stored=False))
