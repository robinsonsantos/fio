#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This module uses the redis
# pub temperature.value
# set temperature.value

import random
import gevent
import redis
from gevent import monkey
monkey.patch_socket()


class Temperature(object):  
    
    def __init__(self):
        pass
        
    def read(self):
        return round(random.uniform(20, 30), 2)          

            
class TemperatureService(object):
    # This needs to refactor    
    REDIS_CONFIG = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        }
        
    def __init__(self):
        self.old_value = None
        self.new_value = None
        self.temperature = Temperature()
        self._redis = redis.StrictRedis(**TemperatureService.REDIS_CONFIG)
    
    def run(self):
        self._redis.set('temperature.value', self.temperature.read())
        
        while True:
            self.new_value = self.temperature.read()
            gevent.spawn(self.publisher)
            gevent.sleep(1)  
            
    def publisher(self):
        if self.new_value != self.old_value:
            self.old_value = self.new_value
            self._redis.set('temperature.value', self.new_value)
            self._redis.publish('temperature.value', self.new_value)        
                  
    
def main():
    temperature_service = TemperatureService()    
    gevent.joinall([gevent.spawn(temperature_service.run)])

if __name__ == '__main__':
    main()        

