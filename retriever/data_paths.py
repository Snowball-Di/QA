# coding:utf-8
"""统一数据文件的路径，因为有好几个地方都会用"""

import os

CURRENT_DIR = os.path.split(os.path.realpath(__file__))[0]

# 文档路径 包含若干jsonl文件 增加的文档可直接放进去
DOCUMENTS_PATH = os.path.join(CURRENT_DIR, 'zh-wiki')

# 文档数据库
DATABASE_PATH = os.path.join(CURRENT_DIR, 'zh-wiki-docs.db')

# TF-IDF稀疏矩阵
DOCS_TFIDF_PATH = os.path.join(CURRENT_DIR, 'docs-tf-idf.npz')

# 中文停用词
ZH_STOPWORDS = os.path.join(CURRENT_DIR, 'stopwords.json')
