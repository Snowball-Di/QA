# coding: utf-8
import json
import base64

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

API_KEY = 'H59sj0jht2kv1YcetcSm46I9'
SECRET_KEY = '6Dr1o9PLXUcx64yqcrpOGeeiyVAG2Nea'
TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'

# ---------------------------------------
# TTS 设置
# ---------------------------------------

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
PER = 4
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 3

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
TTS_FORMAT = FORMATS[AUE]

TTS_CUID = "123456PYTHON"

TTS_URL = 'http://tsn.baidu.com/text2audio'


def tts_fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params).encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read().decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        if not SCOPE in result['scope'].split(' '):
            raise RuntimeError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise RuntimeError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def text2audio(text):
    token = tts_fetch_token()
    tex = quote_plus(text)  # 此处TEXT需要两次urlencode
    print(tex)
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': TTS_CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)
    print('test on Web Browser' + TTS_URL + '?' + data)
    has_error = False

    req = Request(TTS_URL, data.encode('utf-8'))
    try:
        f = urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value) for name, value in f.headers.items())

        has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
    except URLError as err:
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else 'result.' + TTS_FORMAT
    with open(save_file, 'wb') as of:
        of.write(result_str)

    print("has error: ", has_error)
    return result_str


# ---------------------------------------
# ASR 设置
# ---------------------------------------

# 文件格式
ASR_FORMAT = "pcm"

ASR_CUID = '25477966'
# 采样率
RATE = 16000  # 固定值

DEV_PID = 1537  # 1537 表示识别普通话
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'


def asr_fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params).encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        # print('token http response http code : ' + str(err.code))
        result_str = err.read()
        result_str = result_str.decode()

    # print(result_str)
    result = json.loads(result_str)
    # print(result)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        # print(SCOPE)
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise RuntimeError('scope is not correct')
        # print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise RuntimeError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def audio2text(speech_data):
    token = asr_fetch_token()

    length = len(speech_data)
    speech = base64.b64encode(speech_data)
    speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
              'format': ASR_FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': ASR_CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    # print post_data
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        # print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    result_str = str(result_str, 'utf-8')
    print(result_str)
    result = ""
    for i in range(0, len(result_str)):
        if result_str[i] == "[":
            a = i
        if result_str[i] == "]":
            b = i
            break
    result = result_str[a + 2:b - 1]
    return result
