from fastapi import FastAPI, Form ,File, UploadFile
from fastapi.responses import FileResponse
from typing import List
from PIL import Image
import uvicorn
from yolov5 import yoloAnalitics as yolo
import torch
import io
import json
import os
import shutil
from datetime import datetime
import time
from fastapi import APIRouter

router = APIRouter(
    prefix= '/v1/test',
    tags = ['addition']
)

@router.post('/getImagesAnalitics')
async def create_upload_files(file: List[bytes] = File()) :
    if not file:
        return {"message": "No upload file sent"}
    else:
        images = []
        for image in file:
            input_image =Image.open(io.BytesIO(image)).convert("RGB")
            images.append(input_image)
        detectionInfo = yolo.DetectByImagesClassOnly(images)
        json_metadata = json.loads(detectionInfo)
        return json_metadata 

@router.post('/StoreImage')
async def create_upload_files(file:  UploadFile = File(...)) :
    if not file:
        return {"message": "No upload file sent"}
    else:
        originalPath='../DB/Images/Original'
        timeNow= datetime.now()
        timeStamp = str(int(round(timeNow.timestamp())))
        newFileName= timeStamp+'_'+file.filename
        newPath = os.path.join(originalPath,newFileName)
        with open(newPath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
@router.post('/GetNativeMetadata')
async def create_upload_files(file:  UploadFile = File(...)) :
    if not file:
        return {"message": "No upload file sent"}
    else:
        originalPath='../DB/Images/Original'
        timeNow= datetime.now()
        timeStamp = str(int(round(timeNow.timestamp())))
        newFileName= timeStamp+'_'+file.filename
        newPath = os.path.join(originalPath,newFileName)
        with open(newPath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        result = yolo.extractNativeMetadata(newPath)
        return result

@router.post('/UploadImageAndGetImageOverlay')
async def create_upload_files(file:  UploadFile = File(...)) :
    if not file:
        return {"message": "No upload file sent"}
    else:
        originalPath='../DB/Images/Original'
        processedPath='../DB/Images/processed'
        timeNow= datetime.now()
        timeStamp = str(int(round(timeNow.timestamp())))
        newFileName= timeStamp+'_'+file.filename
        OPath = os.path.join(originalPath,newFileName)
        DPath = os.path.join(processedPath,newFileName)
        with open(OPath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        with open(OPath, "rb") as image:
            f = image.read()
            b = bytearray(f)
        input_image =Image.open(io.BytesIO(b)).convert("RGB")
        yolo.saveProcessedImage(input_image,DPath)
        return FileResponse(f"{DPath}/image0.jpg")


       # \\wsl.localhost\Ubuntu-20.04\home\zeev\project\Backend\Backednd\DB\Images\processed\1671198549_traffic.jpg\image0.jpg