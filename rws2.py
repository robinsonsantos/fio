#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

from socketIO_client import SocketIO

REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    }

redis = redis.StrictRedis(**REDIS_CONFIG)
pubsub = redis.pubsub(ignore_subscribe_messages=True)
pubsub.subscribe('pub.notification')

socket = SocketIO('localhost', 5000)

for notification in pubsub.listen():
    print notification['channel']
    print notification['data']
    socket.emit('broadcast event', {'data': notification['data']})
