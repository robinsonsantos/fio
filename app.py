#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='gevent')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('broadcast event', namespace='/test')
def test_broadcast_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('slider event', namespace='/test')
def test_slider_message(message):
    print 'message', message
    #emit('my response', {'data': message['data']}, broadcast=True)
    
if __name__ == '__main__':
    socketio.run(app, debug=True)
