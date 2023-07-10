#!/usr/bin/env python

import time
import base64
import requests
import os
import json
from io import BytesIO
from picamera import PiCamera

cam_image_name = "current_cam.png"
server_ws = os.environ.get("SERVER_WEBSERVICE")
client_name = os.environ.get("CLIENT_NAME")
crop_settings_file_path = "/var/shared_client_volume/settings.json"

"""
Load and return the Crop Settings file and return the object if available
"""
def get_crop_settings():
    if os.path.exists(crop_settings_file_path):
        return json.load(open(crop_settings_file_path))
    else:
        return None

"""
Connect to the camera and do an picture.
"""
def capture():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    time.sleep(2) # Camera warm-up time
    camera.capture(cam_image_name)

"""
Crop the image based on the crop settings
"""
def crop_image_if_needed(image):
    crop_settings = get_crop_settings()
    if crop_settings is None:
        return image.read()
    else:
        buffer = BytesIO()
        image_croped = crop_image_with_settings(image, crop_settings)
        image_croped.save(buffer, type='PNG')
        return buffer.getvalue()

"""
Perform the crop on an image
"""
def crop_image_with_settings(image, settings):
    return image.crop((settings['x'], settings['y'], settings['x2'], settings['y2']))

"""
Send the current_cam image as base64 string to the server-webservice for ocr.
"""
def ocr():
    with open(cam_image_name, "rb") as image_file:
        b64 = base64.b64encode(crop_image_if_needed(image_file))
        o = {
            "client_name": client_name,
            "img_base64": b64.decode('utf-8')
        }
        r = requests.post(server_ws + '/ocr/save', json=o).json()
        print(r)

while True:
    capture()
    ocr()
    time.sleep(60*10)