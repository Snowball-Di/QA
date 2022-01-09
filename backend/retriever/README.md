# :floppy_disk: 文档检索器 Document Retriever

## :star:源代码文件内容

`data_path.py` 提供各种所需的数据的路径

`doc_db.py`  修改自DrQA/drqa/retriever/doc_db.py，简单地封装了对文档数据库的操作

`utils.py` 修改自DrQA/drqa/retriever/utils.py，包括稀疏矩阵存取、哈希、文本清洗等

`run_build_doc_db.py` 修改自DrQA/scripts/retriever/build_doc_db.py，运行它就可以从jsonl文件生成db文件，实现快速获取文档

`run_build_tf-idf.py` 修改自DrQA/scripts/retriever/build_tf_idf.py，运行它就可以生成文档的tf-idf稀疏矩阵和词文档频率，保存到npz文件

`ranker` 修改自DrQA/drqa/retriever/tfidf_doc_ranker.py，检索功能，读取数据文件，向外提供接口

`mytokenizer` 其一是为了统一各处的分词，有一个Tokenizer类，其二提供了tokens的ngram方法

## :star: 数据文件./data/

zh-wiki/目录下是繁体中文维基百科数据，jsonl格式

db文件是文档数据库，表document中，有三个字段id title text，sql操作已经封装在DocDB中

docs-tf-idf.npz文件，由脚本run_build_tf-idf.py生成，由ranker类读取，是检索文档时用到的数据

stopwords.json 文件，是一个缝合版的中文停用词表，检索时会把停用词过滤掉

## :star: 使用接口

实例化时一般不需要填参数，除非需要指定其他数据文件

``` python
from retriever import DocDB, Ranker

database = DocDB()
ranker = Ranker()

query = '我爱北京天安门'
doc_ids = ranker.closest_doc(query, k=5)[0]  # 索引0是文档ID，索引1是文档的相似度分数
title = database.get_doc_title(doc_ids[0])
text = database.get_doc_text(doc_ids[0])
```

:sun_with_face::sun_with_face::sun_with_face::sun_with_face::sun_with_face:

能看到这里，我真的是太爱你啦，给你一个拥抱！

# 🤗
