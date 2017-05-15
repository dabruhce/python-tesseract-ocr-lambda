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

log = logging.getLogger()
log.setLevel(logging.DEBUG)

print('Loading tesseract-lambda')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, 'lib')
PSM = '-l eng -psm 7'
DATA_DIR='--tessdata-dir /var/task/tessdata'
INPUT='/var/task/test.png'
OUTPUT='/tmp/out.txt'

tmp_dir = tempfile.mkdtemp()
tmp_file_name = str('test.txt')
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
        INPUT,
        OUTPUT,
        PSM,
    )

    print('Tesseract command: ' + command)

    try:
        log.debug(command)
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
    print("ver: " + tesserocr.tesseract_version())
    images = ['test.png']
    print("before image file from s3")
    image_file = download_file(bucket, key)
    print("before image file to PIL")
    image = Image.open(image_file)
    print("before OCR")
    result_file = tesseract(image_file)
    upload_file(result_file, bucket, key_name(key))
