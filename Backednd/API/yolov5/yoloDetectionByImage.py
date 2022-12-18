import torch
import json
import numpy as np
from PIL import Image
from io import BytesIO




# Model
def DetectByImage(img):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

    # Images
    #img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list
    #img = './testing/images/traffic.jpg'
    #img = './testing/images/skiVecation1.jpg'

    # Inference
    results = model(img)

    # Results
    #results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
    #results.show()
    jsonData=results.pandas().xyxy[0].to_json(orient="records")  # JSON img1 predictions
    json_object = json.loads(jsonData)
    #print(json.dumps(json_object, indent=1))
    return json.dumps(json_object, indent=1)

def DetectByImageReturnClassOnly(img):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
    results = model(img)
    pdData=results.pandas().xyxy[0]
    pdData=pdData['name'].to_json()
    json_object = json.loads(pdData)
    #print(json.dumps(json_object, indent=1))
    return json.dumps(json_object, indent=1)




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



        

