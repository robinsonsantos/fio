#!/usr/bin/env python

import redis
import gevent
from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

_redis = redis.StrictRedis(**REDIS_CONFIG)
pubsub = _redis.pubsub(ignore_subscribe_messages=True)
pubsub.subscribe('pub.notification')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='gevent')

def publisher():
    while True:
        gevent.sleep(0)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('broadcast event', namespace='/test')
def test_broadcast_message(message):
    for notification in pubsub.listen():
        print notification['channel']
        print notification['data']
        emit('my response', {'data': notification['data']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

