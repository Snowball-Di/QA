#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# 这个文件基本被我从头魔改到尾了
from functools import partial

import numpy as np
import scipy.sparse as sp
import math
from collections import Counter
from tqdm import tqdm
from multiprocessing import Pool as ProcessPool

from . import utils
from . import data_paths
from .doc_db import DocDB
from .mytokenizer import Tokenizer

"""构建TF-IDF文档矩阵"""

database = DocDB()  # 一次性实例化，之后一直用
doc_ids = database.get_doc_ids()  # 从数据库拿到所有文档的id（不是数字），然后把它们映射为索引
doc2index = {doc_id: i for i, doc_id in enumerate(doc_ids)}  # # 这个字典能把文档id映射为索引下标
tokenizer = Tokenizer()
index2tokens_buffer = {}


# ------------------------------------------------------------------------------
# Build article --> word count sparse matrix.
# ------------------------------------------------------------------------------


def get_tokens_of_doc(doc_index):
    """此函数需要按顺序调用"""
    # 尝试分词用batch，但是发现速度不会提升
    seg_batch_size = 32
    global index2tokens_buffer

    if doc_index % seg_batch_size == 0:
        end_index = min(doc_index+seg_batch_size, len(doc_ids))
        docs = [database.get_doc_text(doc_ids[idx]) for idx in range(doc_index, end_index)]
        seg_results = tokenizer.tokenize_batch(docs)
        # 控制字典不占用太多空间
        index2tokens_buffer.clear()
        for idx in range(doc_index, end_index):
            index2tokens_buffer[idx] = seg_results[idx-doc_index]

    tokens = index2tokens_buffer.get(doc_index)
    if tokens is None:
        raise RuntimeError
    else:
        return tokens


def count(ngram, hash_size, doc_id):
    """接受文档id，处理文档文本并返回ngram哈希后的个数，以稀疏矩阵的格式返回"""
    # doc_id = doc_ids[doc_index]
    global doc2index
    doc_index = doc2index[doc_id]
    row, col, data = [], [], []
    title_repeat = (str(database.get_doc_title(doc_id)) + '。') * 3
    tokens = tokenizer.tokenize(title_repeat + database.get_doc_text(doc_id))
    # tokens = get_tokens_of_doc(doc_index)

    # Get ngrams from tokens, with stopwords/punctuation filtering.
    all_ngrams = tokens.ngrams(n=ngram, uncased=True, filter_fn=utils.filter_ngram)

    # Hash ngrams and count occurrences
    counts = Counter([utils.token_hash(gram, hash_size) for gram in all_ngrams])

    # Return in sparse matrix data format.
    row.extend(counts.keys())
    col.extend([doc_index] * len(counts))
    data.extend(counts.values())
    return row, col, data


def get_count_matrix(ngram, hash_size):
    """Form a sparse word to document count matrix (inverted index).

    M[i, j] = # times word i appears in document j.
    """
    row, col, data = [], [], []
    # 分batch多进程，不加多进程的版本在下面的注释里
    workers = ProcessPool(5)
    step = 4096  # 一个batch
    batches = [doc_ids[i:i + step] for i in range(0, len(doc_ids), step)]
    _count = partial(count, ngram, hash_size)
    for batch in tqdm(batches, desc='tokenizing and counting the ngrams', colour='blue'):
        for b_row, b_col, b_data in workers.imap_unordered(_count, batch):
            row.extend(b_row)
            col.extend(b_col)
            data.extend(b_data)
    workers.close()
    workers.join()
    # ````````````````````````````````````````````````````
    # 因为要过模型来分词，这一步会非常的慢
    # for doc_index in tqdm(range(len(doc_ids)), desc='tokenizing and counting the ngrams', colour='blue'):
    #     _row, _col, _data = count(ngram, hash_size, doc_index)
    #     row.extend(_row)
    #     col.extend(_col)
    #     data.extend(_data)

    print('分词，统计ngram已完成，开始创建稀疏矩阵')
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
    # 从计数矩阵统计出词的文档频率DF
    binary = (cnt_matrix > 0).astype(int)
    return np.array(binary.sum(1)).squeeze()


if __name__ == '__main__':
    ngrams = 2  # 论文给的推荐，并不打算修改它
    hash_bucket_size = int(math.pow(2, 26))  # 这是把ngram散列到索引值时，对它取模，以控制矩阵的规模，2^24约为一千六百万

    # 统计ngram个数，返回count矩阵
    count_matrix, doc_dict = get_count_matrix(ngrams, hash_bucket_size)
    # 计算出tf-idf矩阵和词文档频率
    tfidf = get_tfidf_matrix(count_matrix)
    freqs = get_doc_freqs(count_matrix)

    print('Saving to %s' % data_paths.DOCS_TFIDF_PATH)
    metadata = {
        'doc_freqs': freqs,
        'hash_size': hash_bucket_size,
        'ngram': ngrams,
        'doc_dict': doc_dict
    }
    utils.save_sparse_csr(data_paths.DOCS_TFIDF_PATH, tfidf, metadata)
