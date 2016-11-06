'''Server'''
import sqlite3
import uuid
import db
from flask import Flask, jsonify, render_template, request, Response, redirect
import psutil

APP = Flask(__name__)
APP.secret_key = uuid.uuid1()
CONN = db.init_database()

@APP.route('/monitor', methods=['GET'])
def get_page_monitor():
    '''Get page monitor'''
    print(request.cookies)
    if 'token' in request.cookies:
        token = request.cookies.get('token')
        if db.valid_token(CONN, token):
            return render_template('monitor.html')
    return redirect("http://127.0.0.1:5000/signin")

@APP.route('/signin', methods=['GET'])
def get_page_signin():
    '''Get page signin'''
    return render_template('signin.html')

@APP.route('/signin.do', methods=['POST'])
def do_signin():
    '''Sign in'''
    email = request.form['email']
    password = request.form['password']
    if db.valid_user(CONN, email, password):
        token = email + str(uuid.uuid1())
        while not db.add_token(CONN, email, token):
            token = email + str(uuid.uuid1())
        resp = jsonify("success")
        resp.set_cookie("token", token, max_age=360000)
    else:
        resp = jsonify("failed")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@APP.route('/signup.do', methods=['POST'])
def do_signup():
    '''Sign up an account'''
    email = request.form['email']
    password = request.form['password']
    try:
        if db.insert_user(CONN, email, password):
            resp = jsonify("success")
        else:
            resp = jsonify("failed")
    except Exception as e:
        resp = jsonify("failed")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@APP.route('/leave.do', methods=['POST'])
def do_leave():
    '''Leave and destroy cookie'''
    resp = jsonify('success')
    resp.delete_cookie('token')
    return resp

@APP.route('/ram/used', methods=['GET'])
def get_RAM_used():
    '''RAM used'''
    ram = psutil.virtual_memory()
    resp = jsonify(round(ram.used/1024/1024/1024, 2))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@APP.route('/ram/total', methods=['GET'])
def get_RAM_total():
    '''RAM total'''
    ram = psutil.virtual_memory()
    resp = jsonify(round(ram.total/1024/1024/1024, 2))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@APP.route('/cpu/percent', methods=['GET'])
def get_CPU_percent():
    '''CPU percent'''
    resp = jsonify(round(psutil.cpu_percent(), 2))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000)