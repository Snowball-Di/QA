# coding:utf-8
import json
import requests
from colorama import Fore
from flask_cors import CORS
from flask import Flask, request
import struct


def run_server(host=None, port=7982):

    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    @app.route('/api/chat', methods=['POST', 'GET'])
    def fun1():
        try:
            print(Fore.GREEN + '收到问答请求', request.method)
            if request.method == 'POST':
                inputs = json.loads(request.get_data(as_text=True))
                query = inputs['message']

                "/*TODO 接入问答模块 query为问题*/"
                answer = "我已经受到问题啦，问题是"+query

                print('[log] query:', query, 'answer:', answer)
                return json.dumps({'code': 0, 'results': answer}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})

    @app.route('/api/sendaudio', methods=['POST'])
    def fun2():
        try:
            print(Fore.GREEN + '收到音频请求', request.method)
            if request.method == 'POST':
                formdata = request.form
                time = formdata.get('time')
                size = formdata.get('size')
                file = request.files.get('file')
                if file is None:
                    print('文件接收失败')
                    return
                f = open("./test.pcm", "wb")
                audio_data = file.read()
                f.write(audio_data)
                f.close()
                print('[log] audio:', file, 'size:', size, 'time', time)

                "/*TODO: 接入语音识别模块 本地已经存储test.pcm文件 16 16000*/"
                answer = "我已经受到音频请求，时长"+time

                return json.dumps({'code': 0, 'results': answer}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})

    @app.route('/api/sendphoto', methods=['POST'])
    def fun3():
        try:
            print(Fore.GREEN + '收到照片请求', request.method)
            if request.method == 'POST':
                formdata = request.form
                type_ = formdata.get('type')
                file = request.files.get('file')
                if file is None:
                    print('文件接收失败')
                    return
                f = open("./test.jpg", "wb")
                photo_data = file.read()
                f.write(photo_data)
                f.close()
                print('[log] type:', type_)

                "/*TODO: 接入语音识别模块 本地已经存储test.photo文件*/"
                answer = "我已经受到照片请求"

                return json.dumps({'code': 0, 'results': answer}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})

    app.run(host=host, port=port)


def send_request_example():
    res = requests.post("http://localhost:7982/api/chat",
                        data=json.dumps({'message': "北理工的校长？"}))
    print(res.text)


if __name__ == '__main__':
    run_server(host='127.0.0.1')
    print('Exited.')
