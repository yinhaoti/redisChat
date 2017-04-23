from routes import *
from flask import jsonify

import time
import json

main = Blueprint('redischat', __name__)

def current_time():
    return int(time.time())


@main.route('/')
def index_view():
    return render_template('redisChat_index.html')

