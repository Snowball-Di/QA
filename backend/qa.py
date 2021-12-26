# coding:utf-8
import retriever
from reader import Reader


class QA:

    def __init__(self):
        self.database = retriever.DocDB()
        self.ranker = retriever.Ranker()
        self.reader = Reader()

    def __call__(self, question, k_docs=5, cutoff=2048):
        try:
            doc_ids = self.ranker.closest_docs(question, k=5)[0]
        except RuntimeError:
            return '我不明白你在说什么...(无实词)'
        if len(doc_ids) < 1:
            return '我不明白你在说什么...(无匹配项)'

        document = ""
        # 将文章进行拼接，若超长则做截断
        for doc_id in doc_ids:
            document += self.database.get_doc_title(doc_id) + "。" + self.database.get_doc_text(doc_id)
            if len(document) > cutoff:
                break

        outputs = self.reader.pipeline_reader(question, document, top_k=1)
        answer = outputs['answer'] if outputs['answer'] != "" else "不知道"
        return answer

    def simple_ans(self, query):
        doc_id = self.ranker.closest_docs(query, k=1)[0][0]
        document_text = self.database.get_doc_text(doc_id)
        return self.reader.answer(query, document_text)
