

from retriever import DocDB
from retriever import utils
from retriever import mytokenizer


hash_size = pow(2, 26)
code = utils.token_hash('美国', hash_size)
database = DocDB()
tok = mytokenizer.Tokenizer()
print(tok.tokenize('谁改变了美国?').ngrams(n=2, uncased=True, filter_fn=utils.filter_ngram))

document = database.get_doc_text('36885')
print(document)
tokens = tok.tokenize(document)
grams = tokens.ngrams(n=2, uncased=True, filter_fn=utils.filter_ngram)
for g in grams:
    hash_code = utils.token_hash(g, hash_size)
    if hash_code == code:
        print('!!!' + g )  # 真nm撞哈希了，垃圾分词
