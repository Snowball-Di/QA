# 似乎这样用相对导入也没bug
from .. import retriever
from reader import Reader


class QA:

    def __init__(self):
        self.database = retriever.DocDB()
        self.ranker = retriever.Ranker()
        self.reader = Reader()

    def __call__(self, question, k_docs=5):
        self.ranker.closest_docs(question, k_docs)

        # 处理返回的文档id和分数，考虑选取1篇，或者多篇
        best_doc_id = None
        pass

        # 读文档，文档会可能很长，考虑进一步处理
        document = self.database.get_doc_text(best_doc_id)
        print('Document Retrieved:', document)
        outputs = self.reader.pipeline_reader(question, document)

        # 处理pipeline返回的内容
        pass

        return outputs[0]['answer']


if __name__ == '__main__':
    qa_system = QA()
    ans = qa_system('北理工的校长是谁？')
    print(ans)
