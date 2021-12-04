## :star:源代码文件内容

`data_path.py` 

`doc_db.py` 来自drqa/retriever/doc_db.py，简单地封装了对文档数据库的操作

`utils.py` 来自drqa/retriever/utils.py，包括稀疏矩阵存取、哈希、文本清洗等

`run_build_doc_db.py` 来自scripts/retriever，运行它就可以从jsonl文件生成db文件

`run_build_tf-idf.py` 来自scripts/retriever，运行它就可以生成文档的稀疏矩阵和词文档频率，保存到npz文件

`ranker` 来自drqa/retriever/tfidf_doc_ranker.py，检索功能，读取数据文件，向外提供接口



## TODO

