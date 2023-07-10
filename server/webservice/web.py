#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, request
import cv2
import os
import pytesseract
from PIL import Image
import base64
import uuid
import numpy as np
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

"""
Perform OCR on a file
"""
def do_ocr(file_name):
    # Grayscale image for better contrast
    img = Image.open(file_name).convert('L')
    ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
    img = Image.fromarray(img.astype(np.uint8))
    # Run Tesseract on image
    #   Set Page Segmentation Mode = 7 - Treat the image as a single text line
    #   Set char whitelist
    r = pytesseract.image_to_string(img, config="--psm 7 -c tessedit_char_whitelist=0123456789")
    return r.strip() # remove new line

"""
Convert a given value to an int. Also removes leading zeroes during that process.
"""
def convert_to_int(v):
    if not v or v.isdigit() is False:
        return None
    else:
        v = v.lstrip("0") # remove leading 0
        return int(v)

"""
Takes an Base64 String and writes it to a file.
Returns the filename
"""
def write_base64_to_image_file(base64_string):
    file_name = str(uuid.uuid4())
    image = open(file_name, "wb")
    image.write(base64.b64decode(base64_string))
    image.close()
    return file_name

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = os.environ.get("INFLUXDB_URL")
bucket = os.environ.get("INFLUXDB_BUCKET")

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

app = Flask(__name__)

"""
Does OCR and returns the result. Doesn't insert into InfluxDB
"""
@app.route('/ocr', methods=["POST"])
def ocr():
    file_name = write_base64_to_image_file(request.json['img_base64'])

    rFull = do_ocr(file_name)
    rInt = convert_to_int(rFull)
    os.remove(file_name) # remove tmp file
    return {"resultFull": rFull, "resultInt": rInt}

"""
Does OCR and saves it into InfluxDB
"""
@app.route('/ocr/save', methods=["POST"])
def ocr_and_save():
    file_name = write_base64_to_image_file(request.json['img_base64'])

    rFull = do_ocr(file_name)
    rInt = convert_to_int(rFull)
    os.remove(file_name) # remove tmp file
    if rFull is not None or rInt != 0:  
        point = (
            Point("gas")
            .tag("client", request.json['client_name'])
            .field("zahlerstand", rInt)
        )
        write_api.write(bucket=bucket, org="htw", record=point)
        return {"resultFull": rFull, "resultInt": rInt}
    else:
        return {"msg": "Could not extract data from image"}, 400

"""
Simple Status endpoint for health status
"""    
@app.route('/status')
def status():
    return "up", 200

app.run(host='0.0.0.0', port=5002)
