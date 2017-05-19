from __future__ import print_function
from tesserocr import PyTessBaseAPI, PSM
import tesserocr
#import PyTessBaseAPI
import logging
import json
import urllib
import boto3
import os
import subprocess
import tempfile
import uuid
import shutil
import pytesseract
import requests
from PIL import Image



print('Loading tesseract-lambda')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, 'lib')
PSM_FLAG = '-l eng -psm 7'
DATA_DIR='--tessdata-dir /var/task/tessdata'
INPUT='/var/task/test.png'
OUTPUT='/tmp/out.txt'

tmp_dir = tempfile.mkdtemp()
tmp_file_name = str(uuid.uuid4()) + '.txt'
tmp_result_path = os.path.join(tmp_dir, tmp_file_name)
SCRIPT_DIR2 = tmp_dir

s3 = boto3.client('s3')

def download_file(bucket, key):
    path = os.path.join(tmp_dir, key_name(key))
    s3.download_file(bucket, key, path)
    return path

def upload_file(file, bucket, name):
    s3.upload_file(file, bucket, name)

def key_name(key):
    return key.split('/')[-1]

def tesseract(image_file):
    command = 'LD_LIBRARY_PATH={} TESSDATA_PREFIX={} {}/tesseract {} {} {} {}'.format(
        LIB_DIR,
        os.path.join(SCRIPT_DIR, 'tessdata'),
        SCRIPT_DIR2,
        DATA_DIR,
        image_file,
        tmp_result_path,
        PSM_FLAG,
    )

    print('Tesseract command: ' + command)

    try:
        output = subprocess.check_output(command, shell=True)
        print("OUTPUT GOOD 1")
        print(output)
        print("OUTPUT GOOD 2")
        return tmp_result_path
    except subprocess.CalledProcessError as e:
        print(e.output)
        print("OUTPUT BAD")
        raise e

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    shutil.copyfile("tesseract", tmp_dir + '/tesseract')
    shutil.copyfile("test.png", tmp_dir + '/test.png')
    os.chmod(tmp_dir + "/tesseract", 0755)
    os.chmod(tmp_dir, 0755)
    os.chmod('/tmp', 0755)
    print("before image file from s3")
    image_file = download_file(bucket, key)
    print("before image file to PIL")
    print("before OCR")
    result_file = tesseract(image_file)
    print("Print files in firectory")
    for file in os.listdir('/tmp'):
        print(file)
    try:
        print("before PyTessBaseAPI set 2")
        api = PyTessBaseAPI(path=os.path.join(SCRIPT_DIR, 'tessdata'), lang='eng',psm=PSM.AUTO_OSD)
        print("After API set")
        api.SetImageFile(image_file)
        print("After API set image")
        print("TEXT from tesserocr: %s" % api.GetUTF8Text())
        print("CONFIDENCE from tesserocr: %s" % api.AllWordConfidences())
    except Exception:
        pass