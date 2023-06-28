#!/usr/bin/env python

import time
import base64
import requests
import os
from picamera import PiCamera

cam_image_name = "current_cam.png"
server_ws = os.environ.get("SERVER_WEBSERVICE")
client_name = os.environ.get("CLIENT_NAME")

def capture():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    time.sleep(2) # Camera warm-up time
    camera.capture(cam_image_name)

def ocr():
    with open(cam_image_name, "rb") as image_file:
        o = {
            "client_name": client_name,
            "img_base64": base64.b64encode(image_file.read())
        }
        r = requests.post(server_ws + '/ocr/save', json=o).json()
        print(r)

while True:
    capture()
    ocr()
    time.sleep(60*10)