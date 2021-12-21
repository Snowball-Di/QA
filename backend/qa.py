# coding:utf-8
import retriever
from reader import Reader


class QA:

    def __init__(self):
        self.database = retriever.DocDB()
        self.ranker = retriever.Ranker()
        self.reader = Reader()

    def __call__(self, question, k_docs=5):
        try:
            doc_ids = self.ranker.closest_docs(question, k=5)[0]
        except RuntimeError:
            return '我不明白你在说什么...(无实词)'
        if len(doc_ids) < 1:
            return '我不明白你在说什么...(无匹配项)'

        # 处理返回的文档id和分数，考虑选取1篇，或者多篇
        # 读文档，文档会可能很长，考虑进一步处理
        # 直接读 时间会非常长，1024个字符过模型就需要好几秒时间
        document = ""
        for doc_id in doc_ids:
            document += self.database.get_doc_title(doc_id) + "。" + self.database.get_doc_text(doc_id)

        outputs = self.reader.pipeline_reader(question, document, top_k=1)
        answer = outputs['answer'] if outputs['answer'] != "" else "不知道"

        return answer

    def simple_ans(self, query):
        doc_id = self.ranker.closest_docs(query, k=1)[0][0]
        document_text = self.database.get_doc_text(doc_id)
        return self.reader.answer(query, document_text)
