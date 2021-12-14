#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Rank documents with TF-IDF scores"""
import numpy as np
import scipy.sparse as sp

from multiprocessing.pool import ThreadPool
from functools import partial

from . import utils
from . import data_paths
from .doc_db import DocDB
from .mytokenizer import Tokenizer


class TfidfDocRanker(object):

    def __init__(self, tfidf_path=None, strict=True):
        """
        不用传参，用默认的就行
        """
        # 读取稀疏矩阵的npz文件，载入数据
        path = tfidf_path if tfidf_path is not None else data_paths.DOCS_TFIDF_PATH
        print('正在载入文档', path, '这需要一些时间...')
        matrix, metadata = utils.load_sparse_csr(path)
        self.doc_mat = matrix
        print('csr matrix shape:', self.doc_mat.shape)
        self.ngrams = metadata['ngram']
        self.hash_size = metadata['hash_size']
        self.tokenizer = Tokenizer()
        self.doc_freqs = metadata['doc_freqs'].squeeze()
        self.doc_dict = metadata['doc_dict']
        self.num_docs = len(self.doc_dict[0])
        self.strict = strict

    def get_doc_index(self, doc_id):
        """Convert doc_id --> doc_index"""
        return self.doc_dict[0][doc_id]

    def get_doc_id(self, doc_index):
        """Convert doc_index --> doc_id"""
        return self.doc_dict[1][doc_index]

    def closest_docs(self, query, k=1):
        """
        query: 问题字符串
        k: 返回最相似的k个
        返回值为 文档id，文档分数
        """
        sparse_vec = self.text2spvec(query)
        res = sparse_vec * self.doc_mat  # 这里是两个Compressed Sparse Row matrix相乘

        if len(res.data) <= k:
            o_sort = np.argsort(-res.data)
        else:
            o = np.argpartition(-res.data, k)[0:k]
            o_sort = o[np.argsort(-res.data[o])]

        doc_scores = res.data[o_sort]
        doc_ids = [self.get_doc_id(i) for i in res.indices[o_sort]]
        return doc_ids, doc_scores

    def batch_closest_docs(self, queries, k=1, num_workers=None):
        """Process a batch of closest_docs requests multi-threaded.
        Note: we can use plain threads here as scipy is outside of the GIL.
        """
        with ThreadPool(num_workers) as threads:
            closest_docs = partial(self.closest_docs, k=k)
            results = threads.map(closest_docs, queries)
        return results

    def text2spvec(self, query):
        """Create a sparse tfidf-weighted word vector from query.
        tfidf = log(tf + 1) * log((N - Nt + 0.5) / (Nt + 0.5))
        下面的query串预处理，和build tf-idf里47行的处理完全相同
        """
        tokens = self.tokenizer.tokenize(query)
        all_ngrams = tokens.ngrams(n=self.ngrams, uncased=True, filter_fn=utils.filter_ngram)
        wids = [utils.token_hash(gram, self.hash_size) for gram in all_ngrams]

        if len(wids) == 0:
            if self.strict:
                raise RuntimeError('No valid word in: %s' % query)
            else:
                print('No valid word in: %s' % query)
                return sp.csr_matrix((1, self.hash_size))

        # Count TF
        wids_unique, wids_counts = np.unique(wids, return_counts=True)
        tfs = np.log1p(wids_counts)

        # Count IDF
        Ns = self.doc_freqs[wids_unique]
        idfs = np.log((self.num_docs - Ns + 0.5) / (Ns + 0.5))
        idfs[idfs < 0] = 0

        # TF-IDF
        data = np.multiply(tfs, idfs)

        # One row, sparse csr matrix
        indptr = np.array([0, len(wids_unique)])
        spvec = sp.csr_matrix(
            (data, wids_unique, indptr), shape=(1, self.hash_size)
        )
        # 返回稀疏向量，即一个(1, hash_size)的矩阵
        return spvec


if __name__ == '__main__':
    # 测试检索效果，返回top10文档
    ranker = TfidfDocRanker()
    result = ranker.closest_docs('哔哩哔哩动画', k=10)
    database = DocDB()

    for i in range(10):
        print('\ndocument rank', i+1, ' 文档标题:', database.get_doc_title(result[0][i]))
        print('正文：', database.get_doc_text(result[0][i]))
