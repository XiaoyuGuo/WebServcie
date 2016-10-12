#!/usr/bin/python
# -*- coding: utf-8 -*-

'''A server can resize image'''

from flask import Flask, request, make_response, Response
from PIL import Image

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

    image_filename = 'temp' # Create an unique string to identify the image
    image.save(image_filename) # Save image and filename is the unique string before

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
            # Try to resize the image and get content-type
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

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8888)
