'''Server'''
import sqlite3
import service
import uuid
from flask import Flask, jsonify, render_template, request, Response, redirect, send_file
import psutil

APP = Flask(__name__)
APP.secret_key = uuid.uuid1()

@APP.route('/monitor', methods=['GET'])
def get_page_monitor():
    '''Get page monitor'''
    if 'token' in request.cookies:
        token = request.cookies.get('token')
        if service.valid_token(token) == 'success':
            return render_template('monitor.html')
    return redirect("http://127.0.0.1/signin")

@APP.route('/signin', methods=['GET'])
def get_page_signin():
    '''Get page signin'''
    return render_template('signin.html')

@APP.route('/signin.do', methods=['POST'])
def do_signin():
    '''Sign in'''
    email = request.form['email']
    password = request.form['password']
    if service.valid_user(email, password) == 'success':
        token = email + str(uuid.uuid1())
        if service.add_token(email, token) == 'success':
            resp = jsonify("success")
            resp.set_cookie("token", token, max_age=360000)
        else:
            resp = jsonify("failed")
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
        if service.insert_user(email, password) == 'success':
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
    resp = jsonify(service.get_RAM_used())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@APP.route('/ram/total', methods=['GET'])
def get_RAM_total():
    '''RAM total'''
    ram = psutil.virtual_memory()
    resp = jsonify(service.get_RAM_total())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@APP.route('/cpu/percent', methods=['GET'])
def get_CPU_percent():
    '''CPU percent'''
    resp = jsonify(service.get_CPU_percent())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@APP.route('/uploadfile.do', methods=['POST'])
def get_IMG_resize():
    image = request.files['media']
    scale = request.form['scale']
    r = service.get_IMG_resize(image, scale)
    if r.status_code == 200:
        resp = Response(r)
        resp.headers["Content-Disposition"] = "attachment; filename=resize_" + image.filename +";"
        return resp
    else:
        return jsonify("Please input correct image or scale(Integer)")

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000)