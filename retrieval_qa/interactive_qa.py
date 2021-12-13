# coding: utf-8
import os

from colorama import Fore
import qa
from retriever import ltptokenizer



class InteractiveQA(qa.QA):

    def __init__(self):
        super(InteractiveQA, self).__init__()

    def enter(self):
        print(Fore.GREEN + '加载完成，按下任意键进入...')
        os.system('pause')
        do_exit = False
        while not do_exit:
            print(Fore.RESET + '-' * 56)
            print(Fore.LIGHTCYAN_EX + '向人工智障提问 ! 直接输入中文句子, 或输入数字1-30尝试默认问题')
            input_str = input(Fore.BLUE + ' YOU > ')
            if len(input_str) < 1:
                continue
            defaults = [str(i+1) for i in range(0, len(qa.default_questions)-1)]
            if input_str in defaults:
                print(Fore.BLUE + ' YOU : ' + qa.default_questions[int(input_str)])
                self.process(qa.default_questions[int(input_str)])
            elif input_str == 'exit':
                print(Fore.RED + ' BOT : 再见，祝您学业顺利')
                do_exit = True
            else:
                self.process(input_str)

    def process(self, q):
        try:
            doc_ids = self.ranker.closest_docs(q, k=10)[0]
            print(doc_ids)
        except RuntimeError:
            print(Fore.RED + ' BOT : 我不明白你在说什么')
            return
        print(Fore.LIGHTBLACK_EX + '检索到了文档: ', end='')
        for r, did in enumerate(doc_ids):
            print(str(r+1) + '-\"' + self.database.get_doc_title(did) + '\"', end='   ')
        print('\n' + Fore.LIGHTBLACK_EX + '阅读 <\"' + self.database.get_doc_title(doc_ids[0]) + '\"> 以获取答案...')
        document_text = self.database.get_doc_text(doc_ids[0])
        outputs = self.reader.answer(q, document_text)
        print(Fore.RED + ' BOT : ' + outputs)


if __name__ == '__main__':
    bot = InteractiveQA()
    bot.enter()
