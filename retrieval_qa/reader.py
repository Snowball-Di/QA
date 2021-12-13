# coding:utf-8
from functools import partial
import torch
from ltp import LTP
from tqdm import tqdm
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers.pipelines.question_answering import QuestionAnsweringPipeline as QAPipeline


CACHE_DIR = './.model_cache'  # 模型下载缓存到的目录


class Reader:

    def __init__(self, model_name='luhua/chinese_pretrain_mrc_roberta_wwm_ext_large'):
        print('正在载入模型', model_name, ', 这需要一些时间...')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=CACHE_DIR)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name, cache_dir=CACHE_DIR)
        self._hugging_face_pipeline = QAPipeline(model=self.model, tokenizer=self.tokenizer)
        # 使用偏函数固定一部分参数，可以在调用时的kwargs里覆盖其中的任何一个
        self.pipeline = partial(self._hugging_face_pipeline,
                                top_k=2,  # 默认值是1
                                doc_stride=128,  # 默认值是128
                                max_answer_len=128,  # 默认值是15
                                max_seq_len=384,  # 默认值是384
                                max_question_len=64,  # 默认值是64
                                handle_impossible_answer=True  # 默认值是False
                                )

    def answer(self, q, doc):
        """仅返回一个答案字符串"""
        ans = self.pipeline_reader(q, doc, top_k=1)['answer']
        return ans if ans != '' else '不知道'

    def pipeline_reader(self, q, doc, **kwargs):
        """
        以下是QuestionAnsweringPipeline.__call__()方法下的注释，节选过来方便查阅
        这些都是可以调的参数
            topk (:obj:`int`, `optional`, defaults to 1):
                The number of answers to return (will be chosen by order of likelihood). Note that we return less than
                topk answers if there are not enough options available within the context.
            doc_stride (:obj:`int`, `optional`, defaults to 128):
                If the context is too long to fit with the question for the model, it will be split in several chunks
                with some overlap. This argument controls the size of that overlap.
            max_answer_len (:obj:`int`, `optional`, defaults to 15):
                The maximum length of predicted answers (e.g., only answers with a shorter length are considered).
            max_seq_len (:obj:`int`, `optional`, defaults to 384):
                The maximum length of the total sentence (context + question) after tokenization. The context will be
                split in several chunks (using :obj:`doc_stride`) if needed.
            max_question_len (:obj:`int`, `optional`, defaults to 64):
                The maximum length of the question after tokenization. It will be truncated if needed.
            handle_impossible_answer (:obj:`bool`, `optional`, defaults to :obj:`False`):
                Whether or not we accept impossible as an answer.
        :param q: 问题
        :param doc: 文档
        :return: 回答结果，dict类型，若top_k>1则返回List[dict]
        """
        return self.pipeline(question=q, context=doc, **kwargs)


def test_models_with_news():
    document = """11月19日上午，学校召开第一届校务委员会第一次会议。校党委书记、校务委员会主任赵长禄，常务副校长、校务委员会副主任龙腾，校务委员会副主任胡海岩、李和章、杨志宏、方岱宁出席会议，第一届校务委员会委员参加会议。会议由龙腾主持。龙腾介绍了2021年学校事业发展情况和学校“十四五”科技工作设想。与会委员围绕介绍内容进行交流发言，并就人才培养、学科布局、队伍建设、科技创新、校地合作等方面提出了意见和建议。"""
    questions = ['主持人说了什么？',
                 '这次会议是哪个组织召开的？',
                 '谁召开的会？',
                 '谁出席了11月19日的会议？',
                 '谁参加了11月19日的会议？',
                 '与会者做了什么？',
                 '北理工食堂在哪？']

    # 测试NLP工具包LTP的分词功能
    # ltp = LTP('base', cache_dir=CACHE_DIR)
    # seg_result, _ = ltp.seg([document] + questions)  # ltp分词器
    # print(seg_result)

    # 3种模型 创建实例
    roberta_large = Reader(model_name='luhua/chinese_pretrain_mrc_roberta_wwm_ext_large')
    macbert_large = Reader(model_name='luhua/chinese_pretrain_mrc_macbert_large')
    # albert = Reader(model_name='wptoux/albert-chinese-large-qa')

    for i, _q in tqdm(enumerate(questions)):
        print('\n> 问题', i+1, ':', _q)
        print('roberta(1.2G) >', roberta_large.pipeline_reader(_q, document))
        print('macbert(1.2G) >', macbert_large.pipeline_reader(_q, document))
        # print('albert(60M)   >', albert.pipeline_reader(_q, document))


if __name__ == '__main__':
    test_models_with_news()
