# coding: utf-8

from colorama import Fore
import qa
from retriever import mytokenizer


class InteractiveQA(qa.QA):

    def __init__(self):
        super(InteractiveQA, self).__init__()
        self.tok = mytokenizer.Tokenizer()  # 用于显示分词结果，与预测无关
        self._enter()

    def _enter(self):
        print(Fore.GREEN + '加载完成，按下任意键进入...', end='')
        input('')
        print('\n'*20)
        print(Fore.LIGHTCYAN_EX + '-'*10 + '向人工智障提问 ! 直接输入中文句子, 或输入数字1-30' + '-'*10)
        do_exit = False
        while not do_exit:
            input_str = input(Fore.BLUE + ' YOU > ')
            if len(input_str) < 1:
                continue
            if input_str in ['exit', '再见', 'bye', 'goodbye']:
                print(Fore.RED + ' BOT : 再见，祝您学业顺利~')
                do_exit = True
            else:
                self.process(input_str)

    def process(self, q, verbose=True, cutoff=None):
        try:
            doc_ids = self.ranker.closest_docs(q, k=5)[0]
        except RuntimeError:
            print(Fore.RED + ' BOT : 我不明白你在说什么...(无实词)')
            return
        if len(doc_ids) < 1:
            print(Fore.RED + ' BOT : 我不明白你在说什么...(无匹配项)')
            return

        if verbose:
            print(Fore.LIGHTBLACK_EX + '分词处理', self.tok.tokenize(q).data)
            print(Fore.LIGHTBLACK_EX + '检索到的文档: ', end='')
            for r, did in enumerate(doc_ids):
                print(str(r+1) + '-' + str(did) + '-\"' + self.database.get_doc_title(did) + '\"', end='   ')

        document = ""
        for doc_id in doc_ids:
            document += self.database.get_doc_title(doc_id) + "。" + self.database.get_doc_text(doc_id)
            if len(document) > 1024:
                break

        if verbose:
            doc_len = len(document)
            print('\n' + Fore.LIGHTBLACK_EX + '正在阅读 \"' + self.database.get_doc_title(doc_ids[0]) + '\" ('
                  + str(doc_len) + ') 以寻找答案...', end='')
            print(Fore.LIGHTBLACK_EX + '文档正文(节选): ', document[:40])

        if cutoff is not None and len(document) > cutoff:
            if verbose:
                print(Fore.LIGHTBLACK_EX + '文本较长，做简单截断处理，只读前', cutoff, '个字符')
            document = document[:cutoff]

        outputs = self.reader.pipeline_reader(q, document, top_k=1)
        answer = outputs['answer'] if outputs['answer'] != "" else "不知道"
        print(Fore.RED + ' BOT : ' + answer)


if __name__ == '__main__':
    bot = InteractiveQA()
