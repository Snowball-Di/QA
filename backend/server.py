# coding:utf-8
import json

import requests
from colorama import Fore
from flask_cors import CORS
from flask import Flask, request

from qa import QA


def run_server(host=None, port=7982):
    qa_system = QA()

    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    @app.route('/api/chat', methods=['POST', 'GET'])
    def reply():
        try:
            print(Fore.GREEN + '收到请求', request.method)
            if request.method == 'POST':
                inputs = json.loads(request.get_data(as_text=True))
                query = inputs['message']
            else:
                query = request.args.get('query')
            answer = qa_system(query)
            print('[log] query:', query, 'answer:', answer)
            return json.dumps({'code': 0, 'results': answer}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})

    app.run(host=host, port=port)


def send_request_example():
    res = requests.post("http://localhost:7982/api/chat", data=json.dumps({'message': "北理工的校长？"}))
    print(res.text)


if __name__ == '__main__':
    run_server(host='10.195.86.205')
    print('Exited.')
