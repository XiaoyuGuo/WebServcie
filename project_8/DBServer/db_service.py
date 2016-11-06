#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Server of db'''

import json
import db
import requests
from flask import Flask, jsonify, request

APP = Flask(__name__)
CONN = db.init_database()

@APP.route('/valid/user', methods=['POST'])
def valid_user():

    '''Valid user'''

    email = request.form['email']
    password = request.form['password']
    if db.valid_user(CONN, email, password):
        return jsonify('success')
    else:
        return jsonify('failed')

@APP.route('/insert/user', methods=['POST'])
def insert_user():

    '''Insert user'''
    email = request.form['email']
    password = request.form['password']
    if db.insert_user(CONN, email, password):
        return jsonify('success')
    else:
        return jsonify('failed')

@APP.route('/add/token', methods=['POST'])
def add_token():

    '''Add token'''

    email = request.form['email']
    token = request.form['token']
    if db.add_token(CONN, email, token):
        return jsonify('success')
    else:
        return jsonify('failed')

@APP.route('/valid/token', methods=['POST'])
def valid_token():

    '''Valid token'''

    token = request.form['token']
    if db.valid_token(CONN, token):
        return jsonify('success')
    else:
        return jsonify('failed')

def register_service():
    '''Register service in consul'''
    data = {
        "Datacenter": "dc1",
        "Node": "node1",
        "Address": "45.32.101.179",
        "Service": {"Service": "db_service", "Port": 5002, "Address": "127.0.0.1"}
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
    APP.run(host='0.0.0.0', port=5002)