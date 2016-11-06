#!/usr/bin/python
# -*- coding: utf-8 -*-

'''A server can resize image'''

import json
from flask import Flask, request, make_response, Response
from PIL import Image
import requests

APP = Flask(__name__)

@APP.route('/resize', methods=['post'])
def recieve_image():

    '''Recieve image and make a response'''

    resp = make_response()

    scale = request.args.get('scale', 1)

    if 'media' in request.files:
        image = request.files['media']
    else:
        resp.status_code = 400
        return resp

    image_filename = 'temp'
    image.save(image_filename)

    try:
        scale = float(scale)
    except ValueError:
        resp.status_code = 400
        return resp

    if scale == 0:
        resp.status_code = 400
        return resp
    else:
        try:
            image_in = Image.open(image_filename)
        except OSError:
            resp.status_code = 400
            return resp

        image_type = image_in.format
        image_in.close()

        if not image_type in ['JPEG', 'PNG', 'BMP', 'GIF']:
            resp.status_code = 400
            return resp

        if scale == 1:
            pass
        else:
            resize_image(image_filename, scale)

        resp = Response(open(image_filename, 'rb'), content_type='image/' + str(image_type).lower())
        return resp

def resize_image(image_filename, scale):

    '''Resize image'''

    image_in = Image.open(image_filename)

    xsize, ysize = image_in.size
    image_ext = image_in.format

    new_xsize = int(xsize * scale)
    new_ysize = int(ysize * scale)

    image_out = image_in.resize((new_xsize, new_ysize))
    image_in.close()
    image_out.save(image_filename, image_ext)
    image_out.close()

def register_service():
    '''Register service in consul'''
    data = {
        "Datacenter": "dc1",
        "Node": "node2",
        "Address": "45.32.101.179",
        "Service": {"Service": "img_service", "Port": 5003, "Address": "127.0.0.1"}
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
        APP.run(host='0.0.0.0', port=5003)