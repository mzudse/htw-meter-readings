#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, send_file, request
import os
from PIL import Image
import base64
import requests

cam_image_path = "/var/shared_client_volume/current_cam.png" # volume is mounted via docker compose
cam_image_preview_path = "preview.png"
cam_image_preview_settings_path = "settings_scrop_preview.png"
crop_settings_file_path = "/var/shared_client_volume/settings.json"
server_ws = os.environ.get("SERVER_WEBSERVICE")

"""
Load and return the Crop Settings file and return the object if available
"""
def get_crop_settings():
    if os.path.exists(crop_settings_file_path):
        return json.load(open(crop_settings_file_path))
    else:
        return None

"""
Send the given image as base64 string to the server-webservice for ocr and return the result.
"""
def request_ocr(file_name):
    with open(file_name, "rb") as file_image:
        b64 = base64.b64encode(file_image.read())
        o = {
            "img_base64": b64.decode('utf-8')
        }
        r = requests.post(server_ws + '/ocr', json=o).json()
        return {
            "output": {
                "full": r['resultFull'],
                "int": r['resultInt']
            }
        }


"""
Overide the current crop settings
"""
def write_crop_settings(data):
    with open(crop_settings_file_path, "w") as f:
        json.dump(data, f)

app = Flask(__name__)
@app.route('/')
def index():
    return app.send_static_file('index.html')

"""
Returns the current cam image
"""
@app.route('/cam/image')
def cam_image():
    return send_file(cam_image_path)

"""
Perform OCR on the current cam image and return the result
"""
@app.route('/cam/image/ocr')
def cam_image_ocr():
    return request_ocr(cam_image_path)

"""
Wrapper for getting a request get arg
"""
def get_request_arg_value_coords(arg_name):
    return request.args.get(arg_name, default = None, type = int)    

"""
Crop and save the given image
"""
def crop_image_and_save(file_name, x, y, x2, y2):
    img = Image.open(file_name)
    img2 = img.crop((x, y, x2, y2))
    img2.save(cam_image_preview_path)
    img2.close()  

"""
Crop/Resize the preview image and return it
"""
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

"""
Perform OCR on the preview cam image and return the result
"""
@app.route('/cam/image/resize/preview/ocr')
def cam_image_resize_preview_ocr():
    return request_ocr(cam_image_preview_path)

"""
Returns the crop settings if available
"""
@app.route('/settings/crop')
def settings_crop():
    settings = get_crop_settings()
    if settings is None:
        return {"msg": "not crop settings available"}, 404
    else: 
        return settings

"""
Update the crop settings
"""
@app.route('/settings/crop', methods=["POST"])
def settings_crop_save():
    write_crop_settings(request.json)
    return {"msg": "ok"}, 200

"""
Get status of the server-webservice aka ping
"""
def get_restws_status(server):
    try:
        return requests.get(server + 'status', timeout=1).status_code == 200
    except requests.exceptions.RequestException as e:
        return False

"""
Returns the connected server-webservice and its status
"""
@app.route('/app/info')
def app_info():
    return {
        "restws": server_ws,
        "restwsSatus": get_restws_status(server_ws)
    }

"""
Crop based on the settings
"""
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