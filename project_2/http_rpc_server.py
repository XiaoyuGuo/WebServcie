#!/usr/bin/python
# -*- coding: utf-8 -*-

'''This module is a simple rpc server'''
import time as time_lib
import json
import xmltodict
from gevent import monkey, sleep
from gevent.wsgi import WSGIServer
import psutil
from flask import Flask 
from jsonrpc.backend.flask import api

monkey.patch_all()
APP = Flask(__name__)
APP.register_blueprint(api.as_blueprint())

@api.dispatcher.add_method
def time():
    '''
    Return timestamp as type int
    '''
    timestamp = int(time_lib.time())
    sleep(5)
    return timestamp

@api.dispatcher.add_method
def ram():
    '''
    Return ram information
    [total, used] as type [int, int]
    '''
    ram = psutil.virtual_memory()
    total = int(ram.total/1024/1024)
    used = int(ram.used/1024/1024)
    return total, used

@api.dispatcher.add_method
def hdd():
    '''
    Return hdd information
    [total, used] as type [int, int]
    '''
    hdd = psutil.disk_usage('/')
    total = int(hdd.total/1024/1024)
    used = int(hdd.used/1024/1024)
    return total, used

@api.dispatcher.add_method
def add(a, b):
    '''
    Return the result of a + b as type int
    '''
    return a + b

@api.dispatcher.add_method
def sub(a, b):
    '''
    Return the result of a - b as type int
    '''
    return a - b

@api.dispatcher.add_method
def json_to_xml(json_data):
    '''
    Convert json to xml
    '''
    return xmltodict.unparse(json.loads(json_data))

if __name__ == "__main__":
    # Listen port 8088
    #APP.run(host = "0.0.0.0", port = 8088)
    http_server = WSGIServer(("0.0.0.0", 8088), APP)
    http_server.serve_forever()
