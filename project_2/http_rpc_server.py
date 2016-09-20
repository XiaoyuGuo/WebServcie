#!/usr/bin/python
# -*- coding: utf-8 -*-

'''This module is a simple rpc server'''
import time as time_lib
import json
import xmltodict
from gevent import monkey
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
    return timestamp

@api.dispatcher.add_method
def ram():
    '''
    Return ram information
    [total, used] as type [int, int]
    '''
    ram_info = psutil.virtual_memory()
    total = int(ram_info.total/1024/1024)
    used = int(ram_info.used/1024/1024)
    return total, used

@api.dispatcher.add_method
def hdd():
    '''
    Return hdd information
    [total, used] as type [int, int]
    '''
    hdd_info = psutil.disk_usage('/')
    total = int(hdd_info.total/1024/1024)
    used = int(hdd_info.used/1024/1024)
    return total, used

@api.dispatcher.add_method
def add(integer_num_a, integer_num_b):
    '''
    Return the result of integer_num_a + integer_num_b as type int
    '''
    return integer_num_a + integer_num_b

@api.dispatcher.add_method
def sub(integer_num_a, integer_num_b):
    '''
    Return the result of integer_num_a - integer_num_b as type int
    '''
    return integer_num_a - integer_num_b

@api.dispatcher.add_method
def json_to_xml(json_data):
    '''
    Convert json to xml
    '''
    return xmltodict.unparse(json.loads(json_data))

if __name__ == "__main__":
    # Listen port 8088
    #APP.run(host = "0.0.0.0", port = 8088)
    HTTP_SERVER = WSGIServer(("0.0.0.0", 8088), APP)
    HTTP_SERVER.serve_forever()
