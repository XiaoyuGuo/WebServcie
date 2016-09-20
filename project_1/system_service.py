#!/usr/bin/python
# -*- coding: utf-8 -*-

'''This module just is a practice for webservice'''

import time
from flask import Flask, jsonify
import psutil

APP = Flask(__name__)

@APP.route("/time", methods=["GET"])
def get_time():

    '''This function response current timestamp'''

    timestamp = int(time.time())
    return jsonify({"time":timestamp})

@APP.route("/ram", methods=["GET"])
def get_ram():

    '''This function response current ram information'''

    ram = psutil.virtual_memory()
    return jsonify({"total":int(ram.total/1024/1024), "used":int(ram.used/1024/1024)})

@APP.route("/hdd", methods=["GET"])
def get_hdd():

    '''This function response current hdd information'''

    hdd = psutil.disk_usage('/')
    return jsonify({"total":int(hdd.total/1024/1024), "used":int(hdd.used/1024/1024)})

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000)
