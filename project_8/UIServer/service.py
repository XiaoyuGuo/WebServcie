#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Service Module'''

import requests

def valid_user(email, password):

    '''Post form data and get return'''

    data = {
        'email': email,
        'password': password
    }
    resp = requests.post('http://' + get_service_address("db_service") + '/valid/user', data=data)
    if resp.status_code == 200:
        return resp.json()
    else:
        return 'failed'

def insert_user(email, password):

    '''Post form data and get return'''

    data = {
        'email': email,
        'password': password
    }
    resp = requests.post('http://' + get_service_address("db_service") + '/insert/user', data=data)
    if resp.status_code == 200:
        return resp.json()
    else:
        return 'failed'

def add_token(email, token):

    '''Post form data and get return'''

    data = {
        'email': email,
        'token': token
    }
    resp = requests.post('http://' + get_service_address("db_service") + '/add/token', data=data)
    if resp.status_code == 200:
        return resp.json()
    else:
        return 'failed'

def valid_token(token):

    '''Post form data and get return'''

    data = {
        'token': token
    }
    resp = requests.post('http://' + get_service_address("db_service") + '/valid/token', data=data)
    if resp.status_code == 200:
        return resp.json()
    else:
        return 'failed'

def get_RAM_used():

    '''Get RAM used from server'''

    resp = requests.get('http://' + get_service_address("system_info") + '/ram/used')
    if resp.status_code == 200:
        return resp.json()
    else:
        return 0

def get_RAM_total():

    '''Get RAM total from server'''

    resp = requests.get('http://' + get_service_address("system_info") + '/ram/total')
    if resp.status_code == 200:
        return resp.json()
    else:
        return 0

def get_CPU_percent():

    '''Get CPU percent from server'''

    resp = requests.get('http://' + get_service_address("system_info") + '/cpu/percent')
    if resp.status_code == 200:
        return resp.json()
    else:
        return 0

def get_IMG_resize(image, scale):

    '''Get IMG resize'''

    r = requests.post('http://' + get_service_address("img_service") + '/resize?scale=' + scale +'', files={'media': image})
    return r

def get_service_address(service_name):

    '''Get service name'''

    response = requests.get("http://127.0.0.1:8500/v1/catalog/service/" + service_name)
    if not response.status_code == 200:
        return False
    service_info = response.json()[0]
    address = service_info["ServiceAddress"] + ":" + str(service_info["ServicePort"])
    return address