# coding: utf-8
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

current_id = 0
passage_len_dict = {}


def preprocess(article):
    # 有很多没有正文的页面，丢弃
    if article['text'] == '':
        return None
    # 标题带"（消歧义）"的
    if disambiguation in article['title']:
        return None
    # 繁体中文转为简体中文
    # passage_title = article['title']
    # passage_text = article['text']
    passage_title = converter.convert(article['title'])
    passage_text = converter.convert(article['text'])

    # # 用于统计文章长度分布
    # global passage_len_dict
    # if passage_len_dict.get(int(len(passage_text))) is None:
    #     passage_len_dict[int(len(passage_text))] = 1
    # else:
    #     passage_len_dict[int(len(passage_text))] = passage_len_dict[int(len(passage_text))] + 1

    global current_id
    current_id += 1

    return {'id': current_id, 'title': passage_title, 'text': passage_text}


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
            doc = json.loads(line)
            # 按换行符进行拆分
            paragraphs = doc['text'].split('\n')
            # 超出一定长度的拆为两篇
            cut = []
            for paragraph in paragraphs:
                while len(paragraph) > 700:
                    cut.append(paragraph[:700])
                    paragraph = paragraph[700:]
                cut.append(paragraph)
            # 遍历拆分后的段落
            for paragraph in cut:
                # 将标题和拆分段落 送预处理函数
                ret = preprocess({'title': doc['title'], 'text': paragraph})
                if not ret:
                    continue
                # 保存三元组
                documents.append((ret['id'], ret['title'], ret['text']))
    return documents


def store_contents(data_path, save_path, num_workers=1):
    """Preprocess and store a corpus of documents in sqlite.

    Args:
        data_path: Root path to directory (or directory of directories) of files
          containing json encoded documents (must have `id` and `text` fields).
        save_path: Path to output sqlite db.
        num_workers: Number of parallel processes to use when reading docs.
        因为编制id作为数据库主键，会涉及到进程同步问题，因为我不想去查怎么用semaphor同步进程了，所以干脆就别整了
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
    with tqdm(total=len(files), colour='green') as bar:
        # multi process:
        # for tuples in workers.imap_unordered(get_contents, files):
        #     count += len(tuples)
        #     c.executemany("INSERT INTO documents VALUES (?,?,?)", tuples)
        #     bar.update()
        # single process:
        for filename in files:
            tuples = get_contents(filename)
            count += len(tuples)
            c.executemany("INSERT INTO documents VALUES (?,?,?)", tuples)
            bar.update()

    logger.info('Read %d docs.' % count)
    logger.info('Committing...')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    store_contents(data_paths.DOCUMENTS_PATH, data_paths.DATABASE_PATH, num_workers=4)

    # with open('save.json', 'w') as f:
    #     f.write(json.dumps(passage_len_dict))
