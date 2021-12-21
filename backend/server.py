# coding:utf-8
import json

import requests
from colorama import Fore
from flask_cors import CORS
from flask import Flask, request

from qa import QA


def run_server(port=7982):
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
            return json.dumps({'code': 0, 'results': qa_system(query)}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})

    app.run(host='10.62.58.199', port=port,)


def send_request():
    res = requests.post("http://10.195.48.145:7892/api/chat", data=json.dumps({'message': "北理工的校长？"}))
    print(res.text)


if __name__ == '__main__':
    run_server()
    print('Exited.')
