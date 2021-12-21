#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""读取jsonl文本，以id-text的形式储存到数据库"""
# 这个文件基本被我从头魔改到尾了

import sqlite3
import json
import os
import logging

from multiprocessing import Pool as ProcessPool
from tqdm import tqdm
from opencc import OpenCC

import data_paths

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)

converter = OpenCC('t2s.json')
disambiguation = converter.convert('消歧义')

current_doc_id = 0


def preprocess(article):
    """
    用于清洗文本的函数，输入为单行json解析后的对象
    """
    # 有很多没有正文的页面，丢弃
    if article['text'] == '':
        return None
    # 标题带[（消歧义）]的
    if disambiguation in article['title']:
        return None
    global current_doc_id
    current_doc_id += 1
    # 繁体中文转为简体中文
    # return {'id': article['id'], 'title': converter.convert(article['title']),
    #         'text': converter.convert(article['text'])}
    return {'id': current_doc_id, 'title': converter.convert(article['title']),
            'text': converter.convert(article['text'])}


# ------------------------------------------------------------------------------
# Store corpus.
# ------------------------------------------------------------------------------


def iter_files(path):
    """这个函数能够迭代一个目录路径下的所有文件"""
    """Walk through all files located under a root path."""
    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                yield os.path.join(dirpath, f)
    else:
        raise RuntimeError('Path %s is invalid' % path)


def get_contents(filename):
    """输入jsonl文件，解析并预处理（过滤），拿出文档id和文档文本返回"""
    documents = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            doc = preprocess(json.loads(line))
            if not doc:
                continue
            # Add the document
            documents.append((doc['id'], doc['title'], doc['text']))
    return documents


def store_contents(data_path, save_path, num_workers=1):
    """Preprocess and store a corpus of documents in sqlite.

    Args:
        data_path: Root path to directory (or directory of directories) of files
          containing json encoded documents (must have `id` and `text` fields).
        save_path: Path to output sqlite db.
        num_workers: Number of parallel processes to use when reading docs.
    """
    if os.path.isfile(save_path):
        raise RuntimeError('%s already exists! Not overwriting.' % save_path)

    logger.info('Reading into database...')
    conn = sqlite3.connect(save_path)
    c = conn.cursor()
    c.execute("CREATE TABLE documents (id PRIMARY KEY, title, text);")

    workers = ProcessPool(num_workers)
    files = [f for f in iter_files(data_path)]
    count = 0
    with tqdm(total=len(files)) as pbar:
        for tuples in workers.imap_unordered(get_contents, files):
            count += len(tuples)
            c.executemany("INSERT INTO documents VALUES (?,?,?)", tuples)
            pbar.update()
    logger.info('Read %d docs.' % count)
    logger.info('Committing...')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    store_contents(data_paths.DOCUMENTS_PATH, data_paths.DATABASE_PATH, num_workers=4)
