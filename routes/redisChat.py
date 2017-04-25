from routes import *
from flask import jsonify
from app import stream, chat_channel, red
from utils import log

import time
import json

main = Blueprint('redischat', __name__)

def current_time():
    return int(time.time())


@main.route('/')
def index_view():
    return render_template('redisChat_index.html')


@main.route('/subscribe')
def subscribe():
    log('success use subscribe')
    return Response(stream(), mimetype="text/event-stream")



@main.route('/chat/add', methods=['POST'])
def chat_add():
    # 当 content-type 是application/json 的时候
    # 我们用 get_json() 得到一个字典  flask帮我们解析了
    # 如果是平板 ios android， 数据传送的方式就不是表单了，是这种
    msg = request.get_json()
    name = msg.get('name', '<匿名>')
    content = msg.get('content', '')
    channel = msg.get('channel', '')
    r = {
        'name': name,
        'content': content,
        'channel': channel,
        'created_time': current_time(),
    }
    message = json.dumps(r, ensure_ascii=False)
    print('debug', message)
    # 用redis发布消息
    red.publish(chat_channel, message)
    return 'OK'