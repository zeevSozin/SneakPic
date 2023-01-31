import torch
import json
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
import io
import pandas as pd
import base64
from io import BytesIO

## picture native metadata extraction


def extractNativeMetadata(imageFile):
    nativeMetadata = {}
    image = Image.open((imageFile))
    exifdata = image.getexif()
    for tagid in exifdata:
        tagname = TAGS.get(tagid, tagid)
        value = exifdata.get(tagid)
        nativeMetadata.update({f"{tagname}":f"{value}"})
    return nativeMetadata



def DetectByImage(img):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
    results = model(img)
    jsonData=results.pandas().xyxy[0].to_json(orient="records")  # JSON img1 predictions
    json_object = json.loads(jsonData)
    return json.dumps(json_object, indent=1)

def DetectByImageReturnClassOnly(img):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
    results = model(img)
    pdData=results.pandas().xyxy[0].value_counts('name').to_json()
    json_object = json.loads(pdData)
    return json_object


def saveProcessedImage(img,destinationDir):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
    results = model(img)
    results.save(save_dir=destinationDir)

def GetProccesedImabeasBase64(img):
     model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
     result = model(img)
     bufferd = BytesIO()
     result.save(bufferd)
     return bufferd
     

def DetectByImages(images):
    result=list()
    if(len(images) == 0):
        return "No images added"
    else:
        for img in images:
            res=DetectByImage(img)
            result.append(res)
        json_result = json.loads(result)
        return json.dumps(json_result, indent = 1)

def DetectByImagesClassOnly(images):
    if(len(images) == 0):
        return "No images added"
    elif (len(images) == 1):
        return DetectByImageReturnClassOnly(images)
    else:
        resultArry=[]
        for img in images:
            result = DetectByImageReturnClassOnly(img)
            json_obj = json.loads(result)
            resultArry.append(json_obj)
        return json.dumps(resultArry, indent = 2)

def GetProcessedImage(image):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    result = model(image)
    return result

     

