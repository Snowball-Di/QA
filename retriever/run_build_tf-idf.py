#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# 这个文件基本被我从头魔改到尾了

import numpy as np
import scipy.sparse as sp
import math
import logging
from collections import Counter

import utils
import data_paths
from doc_db import DocDB

"""构建TF-IDF文档矩阵"""

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)

doc2index = {}  # 到索引的映射，会在读取的时候初始化
tokenizer = None
database = DocDB()  # 一次性实例化，之后一直用


def tokenize(text):
    global tokenizer
    return tokenizer.tokenize(text)


# ------------------------------------------------------------------------------
# Build article --> word count sparse matrix.
# ------------------------------------------------------------------------------


def count(ngram, hash_size, doc_id):
    """接受文档id，处理文档文本并返回ngram哈希后的个数，以稀疏矩阵的格式返回"""
    row, col, data = [], [], []
    # Tokenize
    tokens = tokenize(database.get_doc_text(doc_id))

    # Get ngrams from tokens, with stopwords/punctuation filtering.
    all_ngrams = tokens.ngrams(n=ngram, uncased=True, filter_fn=utils.filter_ngram)

    # Hash ngrams and count occurrences
    counts = Counter([utils.token_hash(gram, hash_size) for gram in all_ngrams])

    # Return in sparse matrix data format.
    row.extend(counts.keys())
    col.extend([doc2index[doc_id]] * len(counts))
    data.extend(counts.values())
    return row, col, data


def get_count_matrix(ngram, hash_size):
    """Form a sparse word to document count matrix (inverted index).

    M[i, j] = # times word i appears in document j.
    """
    # 从数据库拿到所有文档的id（不是数字），然后把它们映射为索引
    doc_ids = database.get_doc_ids()
    global doc2index
    doc2index = {doc_id: i for i, doc_id in enumerate(doc_ids)}

    row, col, data = [], [], []
    for doc_id in doc_ids:
        _row, _col, _data = count(ngram, hash_size, doc_id)
        row.extend(_row)
        col.extend(_col)
        data.extend(_data)

    logger.info('Creating sparse matrix...')
    count_csr_matrix = sp.csr_matrix(
        (data, (row, col)), shape=(hash_size, len(doc_ids))
    )
    count_csr_matrix.sum_duplicates()
    return count_csr_matrix, (doc2index, doc_ids)


# ------------------------------------------------------------------------------
# Transform count matrix to different forms.
# ------------------------------------------------------------------------------


def get_tfidf_matrix(cnt_matrix):
    """Convert the word count matrix into tfidf one.

    tfidf = log(tf + 1) * log((N - Nt + 0.5) / (Nt + 0.5))
    * tf = term frequency in document
    * N = number of documents
    * Nt = number of occurrences of term in all documents
    """
    Ns = get_doc_freqs(cnt_matrix)
    idfs = np.log((cnt_matrix.shape[1] - Ns + 0.5) / (Ns + 0.5))
    idfs[idfs < 0] = 0
    idfs = sp.diags(idfs, 0)
    tfs = cnt_matrix.log1p()
    tfidfs = idfs.dot(tfs)
    return tfidfs


def get_doc_freqs(cnt_matrix):
    """Return word --> # of docs it appears in."""
    binary = (cnt_matrix > 0).astype(int)
    freqs = np.array(binary.sum(1)).squeeze()
    return freqs


if __name__ == '__main__':
    ngrams = 2  # 论文给的推荐，并不打算修改它
    hash_bucket_size = int(math.pow(2, 24))  # 这是把ngram散列到索引值时，对它取模，以控制矩阵的规模，2^24约为一千六百万

    logging.info('Counting words...')
    count_matrix, doc_dict = get_count_matrix(ngrams, hash_bucket_size)

    logger.info('Making tfidf vectors...')
    tfidf = get_tfidf_matrix(count_matrix)

    logger.info('Getting word-doc frequencies...')
    freqs = get_doc_freqs(count_matrix)

    logger.info('Saving to %s' % data_paths.DOCS_TFIDF_PATH)
    metadata = {
        'doc_freqs': freqs,
        'hash_size': hash_bucket_size,
        'ngram': ngrams,
        'doc_dict': doc_dict
    }
    utils.save_sparse_csr(data_paths.DOCS_TFIDF_PATH, tfidf, metadata)
