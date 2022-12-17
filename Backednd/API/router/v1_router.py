from fastapi import FastAPI, Form ,File, UploadFile
from fastapi.responses import FileResponse
from typing import List
from PIL import Image
from yolov5 import yoloAnalitics as yolo
import torch
import io
import json
import os
import shutil
from datetime import datetime
from fastapi import APIRouter
from utills import dbUtills
from Localmodels import album

db='test-db'
pictureCollection="pictures"
albumCollection = "albums"

router = APIRouter(
    prefix= '/v1',
    tags = ['addition']
)


@router.post("/getMetadataSinleImage/")
async def create_upload_file(file: bytes = File(...)) :
    if not file:
        return {"message": "No upload file sent"}
    else:
        images = []
        input_image =Image.open(io.BytesIO(file)).convert("RGB")
        images.append(input_image)
        detectionInfo = yolo.DetectByImagesClassOnly(images)
        json_metadata = json.loads(detectionInfo) 
        return json_metadata

@router.post("/getMetadaMultipleImages/")
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


@router.post("/uploadSingleImage/")
async def create_upload_files(file:  bytes = File(...)) :
    if not file:
        return {"message": "No upload file sent"}
    else:
        images = []
        originalPath='./DB/Images/Original'
        
        nativeMetadata = yolo.extractNativeMetadata(file)
        return nativeMetadata












@router.post("/printDetectedSinleImage/")
async def create_upload_file(file: bytes = File(...)) :
    if not file:
        return {"message": "No upload file sent"}
    else:
        images = []
        input_image =Image.open(io.BytesIO(file)).convert("RGB")
        images.append(input_image)
        imageWithOverlay = yolo.PrintDetectedImage(images)
        
        return imageWithOverlay.show()
