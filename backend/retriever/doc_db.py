#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import sqlite3
try:
    from . import data_paths
except ImportError:
    import data_paths

"""提供DocDB类,封装数据库的操作"""


class DocDB(object):

    def __init__(self, db_path=None):
        self.path = db_path or data_paths.DATABASE_PATH
        self.connection = sqlite3.connect(self.path, check_same_thread=False)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        self.close()  # 析构的时候自动关闭连接

    def path(self):
        """Return the path to the file that backs this database."""
        return self.path

    def close(self):
        """Close the connection to the database."""
        self.connection.close()

    def get_doc_ids(self):
        """Fetch all ids of docs stored in the db."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM documents")
        results = [r[0] for r in cursor.fetchall()]
        cursor.close()
        return results

    def get_doc_title(self, doc_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT title FROM documents WHERE id = ?", (doc_id,))
        result = cursor.fetchone()
        cursor.close()
        return result if result is None else result[0]

    def get_doc_text(self, doc_id):
        """Fetch the raw text of the doc for 'doc_id'."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT text FROM documents WHERE id = ?", (doc_id,))
        result = cursor.fetchone()
        cursor.close()
        return result if result is None else result[0]
