#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, send_file, request
import os
from PIL import Image
import base64
import requests

cam_image_path = "../watcher/current_cam.png"
cam_image_preview_path = "../preview.png"
cam_image_preview_settings_path = "../settings_scrop_preview.png"
crop_settings_file_path = "../settings.json"
server_ws = os.environ.get("SERVER_WEBSERVICE")


def get_current_img():
    return 123 # todo PiCamera

def get_crop_settings():
    if os.path.exists(crop_settings_file_path):
        return json.load(open(crop_settings_file_path))
    else:
        return None

def request_ocr(fileName):
    with open(fileName, "rb") as image_file:
        o = {
            "img_base64": base64.b64encode(image_file.read())
        }
        r = requests.post(server_ws + '/ocr', json=o).json()
        return {
            "output": {
                "full": r['resultFull'],
                "int": r['resultInt']
            }
        }

def write_crop_settings(data):
    with open(crop_settings_file_path, "w") as f:
        json.dump(data, f)

app = Flask(__name__)
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/cam/image')
def cam_image():
    return send_file(cam_image_path)

@app.route('/cam/image/ocr')
def cam_image_ocr():
    return request_ocr(cam_image_path)

def get_request_arg_value_coords(arg_name):
    return request.args.get(arg_name, default = None, type = int)    

def crop_image_and_save(file_name, x, y, x2, y2):
    img = Image.open(file_name)
    img2 = img.crop((x, y, x2, y2))
    img2.save(cam_image_preview_path)
    img2.close()  

@app.route('/cam/image/resize/preview')
def cam_image_resize_preview():
    x = get_request_arg_value_coords('x')
    y = get_request_arg_value_coords('y')
    x2 = get_request_arg_value_coords('x2')
    y2 = get_request_arg_value_coords('y2')
    if None in (x, y, x2, y2):
        return {"msg": "invalid params"}, 400    
    
    crop_image_and_save(cam_image_path, x, y, x2, y2)
    return send_file(cam_image_preview_path)

@app.route('/cam/image/resize/preview/ocr')
def cam_image_resize_preview_ocr():
    return request_ocr(cam_image_preview_path)

@app.route('/settings/crop')
def settings_crop():
    settings = get_crop_settings()
    if settings is None:
        return {"msg": "not scrop settings available"}, 404
    else: 
        return settings

@app.route('/settings/crop', methods=["POST"])
def settings_crop_save():
    write_crop_settings(request.json)
    return {"msg": "ok"}, 200

def get_restws_status(server):
    try:
        return requests.get(server + 'status', timeout=1).status_code == 200
    except requests.exceptions.RequestException as e:
        return False

@app.route('/app/info')
def app_info():
    return {
        "restws": server_ws,
        "restwsSatus": get_restws_status(server_ws)
    }

@app.route('/settings/crop/preview')
def settings_scrop_preview():
    img = Image.open(cam_image_path)
    settings = get_crop_settings()
    if settings is not None:
        img2 = img.crop((settings['x'], settings['y'], settings['x2'], settings['y2']))
        img2.save(cam_image_preview_settings_path)
        img.close()
        return send_file(cam_image_preview_settings_path)
    else:
        img.close()
        return send_file(img)

app.run(host='0.0.0.0', port=5004)