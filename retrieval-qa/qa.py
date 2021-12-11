# 似乎这样用相对导入也没bug
import time

import retriever
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

    def simple_ans(self, query):
        start_time = time.process_time()
        doc_id = self.ranker.closest_docs(query, k=1)[0][0]
        document_text = self.database.get_doc_text(doc_id)
        outputs = self.reader.answer(query, document_text)
        # print('time cost:', time.process_time()-start_time)
        return outputs


if __name__ == '__main__':
    qa_system = QA()
    questions = ['天安门在哪？',
                 '习近平在哪里出生？',
                 '贝多芬于哪里出生？',
                 '鲲鹏处理器是什么？',
                 '猫有几条腿？',
                 '为什么我复习不完？',
                 '牛顿三定律是什么？',
                 '1453年发生了什么？',
                 '苹果手机是哪一年发布的？',
                 '什么是苹果手机？',
                 '什么是中央处理器？',
                 '摩尔定律是什么？',
                 '什么是人工智能？',
                 '什么是哥德巴赫猜想？',
                 '什么是有限状态机?',
                 '什么是黎曼猜想?',
                 '刘华强是谁？',
                 '蜜雪冰城是什么?']

    for i, q in enumerate(questions):
        print('问题', i, ':', q)
        print('    ', qa_system.simple_ans(q))
