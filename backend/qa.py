# coding:utf-8
import base64
import time

from colorama import Fore

import retriever
import reader
from audio import text2audio

# --------------------------------------------------
# 新版QA模块 - 设置
# --------------------------------------------------

# 检索器返回的段数，每段上限为700字，平均约75字，实际平均值可能超过100字
# 阅读模型的执行速度与它成正比
# 虽然理论上值越大越精准，但是目前的阅读器模型并没有处理多文档的能力
PASSAGE_TOP_K = 20
# 问答回复类型
INVALID_NO_WORD = 0x0001
INVALID_NO_MATCH_DOC = 0x0002
ANSWER_IMPOSSIBLE = 0x0010
ANSWER_DEFINITE = 0x0020
ANSWER_NOT_SURE = 0x0040
# 超过这个分数（代表有把握）就返回definite
THRESHOLD = 0.5
# 是否在控制台输出详细信息
verbose = True
# 拼接文档的总长度限制
max_context_length = 2048
# 是否使用多文档分别过pipeline
separate_read = False


def generate_reply(msg_type, question_text=None, answer_text=None) -> dict:
    if verbose:
        print('应答类型: %d' % msg_type, '; 问题: %s' % question_text, '; 答案: %s' % answer_text)

    audio_data = text2audio(answer_text)
    audio_bytes = base64.b64encode(audio_data)

    reply_dict = {'code': 0,
                  'type': msg_type,
                  'question': question_text,
                  'text': answer_text,
                  'audio': str(audio_bytes, 'ascii')}
    return reply_dict


class Qa:

    def __init__(self):
        self.database = retriever.DocDB()
        self.ranker = retriever.Ranker()
        self.reader = reader.Reader()

    def answer(self, query: str) -> dict:
        start_time = time.process_time()
        try:
            doc_ids, scores = self.ranker.closest_docs(query, k=PASSAGE_TOP_K)
        except RuntimeError:
            return generate_reply(INVALID_NO_WORD, query, "我不明白...")
        if len(doc_ids) < 1:
            return generate_reply(INVALID_NO_MATCH_DOC, query, "我不明白...")

        if separate_read:
            # 逐个阅读 检索器返回的多个文档段落，选出分数最高的结果
            result = {'answer': "", 'score': float(0), }  # 默认是无答案IMPOSSIBLE
            for doc_id in doc_ids:
                context_read = str(self.database.get_doc_title(doc_id) + '。') * 3 + \
                               self.database.get_doc_text(doc_id)
                candidate_result = self.reader.pipeline_reader(query, context_read, top_k=1)
                if verbose:
                    print('文档检索结果: ', context_read)
                    print('阅读器输出:', candidate_result)
                if candidate_result['answer'] != "" and candidate_result['score'] > result['score']:
                    # result = {'answer': candidate_result['answer'], 'score': candidate_result['score']}
                    result = dict(candidate_result)
            if verbose:
                print('处理耗时: %f s.' % (time.process_time() - start_time))
        else:
            context = ""
            for doc_id in doc_ids:
                context += str(self.database.get_doc_title(doc_id) + '。') + \
                           self.database.get_doc_text(doc_id)
                if len(context) > max_context_length:
                    break
            result = self.reader.pipeline_reader(query, context, top_k=1)
            if verbose:
                print('文档检索结果: ', context)
                print('阅读器输出:', result)
                print('处理耗时: %f s.' % (time.process_time() - start_time))

        # 生成应答信息
        if result['answer'] == "":
            return generate_reply(ANSWER_IMPOSSIBLE, query, "我不知道...")
        elif result['score'] > THRESHOLD:
            return generate_reply(ANSWER_DEFINITE, query, result['answer'])
        else:
            return generate_reply(ANSWER_NOT_SURE, query, result['answer'])


class Interactive(Qa):
    """用于问答系统的测试"""

    def __init__(self):
        super(Interactive, self).__init__()

    def enter(self):
        print(Fore.GREEN + '加载完成，按下任意键进入...', end='')
        input('')
        while True:
            input_str = input(Fore.BLUE + ' YOU > ' + Fore.LIGHTWHITE_EX)
            if len(input_str) < 1:
                continue
            else:
                print(Fore.RED, self.answer(input_str))


if __name__ == '__main__':
    questions = [
        '北理工的校长是谁？',
        '北理工的校长是？',
        '北理工的校长是',
        '北理工的校长',
        '北理工校长',
        '北京理工大学的校长是谁？',
        '北京理工大学的校长',
        '北京理工大学校长',
        '北理的校长是谁？',
        '北理的校长？',
        '北理校长',
        '北理工的校训是什么？',
        '中国的首都在哪',
        '机器学习是什么',
        '谁发明了第一台计算机',
        '什么是牛顿三定律？',
        '北京理工大学在哪？',
        '烟台在哪',
        '中国共产党于何时成立？',
        '轴心国有哪些',
        '蜜雪冰城是什么？'
    ]

    qa_system = Interactive()
    for q in questions:
        print(qa_system.answer(q))
    qa_system.enter()
