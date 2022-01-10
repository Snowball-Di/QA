# coding:utf-8
import json
import requests
from colorama import Fore
from flask_cors import CORS
from flask import Flask, request
import struct
import face_recognition

from audio import audio2text
from qa import Qa


def run_server(host=None, port=7982):
    qa_module = Qa()

    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    @app.route('/api/chat', methods=['POST', 'GET'])
    def fun1():
        try:
            print(Fore.GREEN + '收到问答请求', request.method)
            if request.method == 'POST':
                inputs = json.loads(request.get_data(as_text=True))
                # 执行问答模块，返回答案文本、答案音频、应答类型
                reply_data = qa_module.answer(str(inputs['message']))
                return json.dumps(reply_data, ensure_ascii=False)
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

                # 语音识别，输入文件，返回文本
                asr_text = audio2text(audio_data)

                return json.dumps({'code': 0, 'results': asr_text}, ensure_ascii=False)
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
                photo_data = file.read()
                temp_path = "./recognition.jpg"
                with open(temp_path, "wb") as f:
                    f.write(photo_data)
                print('[log] type:', type_)

                # 图像输入，人脸检测，返回是否有人脸
                image = face_recognition.load_image_file(temp_path)
                num_of_face = len(face_recognition.face_locations(image))
                flag = True if num_of_face > 0 else False

                return json.dumps({'code': 0, 'results': flag}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})

    app.run(host=host, port=port)


def send_request_example():
    res = requests.post("http://localhost:7982/api/chat",
                        data=json.dumps({'message': "北理工的校长？"}))
    print(res.text)


if __name__ == '__main__':
    run_server(host='192.168.176.51')
    print('Exited.')
