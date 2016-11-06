#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Server of ram and cpu'''

import json
import requests
from flask import Flask, jsonify
import psutil

APP = Flask(__name__)

@APP.route('/ram/used', methods=['GET'])
def get_RAM_used():
    '''RAM used'''
    ram = psutil.virtual_memory()
    return jsonify(round(ram.used/1024/1024/1024, 2))

@APP.route('/ram/total', methods=['GET'])
def get_RAM_total():
    '''RAM total'''
    ram = psutil.virtual_memory()
    return jsonify(round(ram.total/1024/1024/1024, 2))

@APP.route('/cpu/percent', methods=['GET'])
def get_CPU_percent():
    '''CPU percent'''
    return jsonify(round(psutil.cpu_percent(), 2))

def register_service():
    '''Register service in consul'''
    data = {
        "Datacenter": "dc1",
        "Node": "node",
        "Address": "45.32.101.179",
        "Service": {"Service": "system_info", "Port": 5001, "Address": "127.0.0.1"}
        }
    response = requests.put(
        "http://127.0.0.1:8500/v1/catalog/register",
        data=json.dumps(data)
        )
    if response.status_code == 200:
        return True
    return False

if __name__ == '__main__':
    if register_service():
        print("Register service successful")
        APP.run(host='0.0.0.0', port=5001)