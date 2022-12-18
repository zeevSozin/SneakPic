from fastapi import FastAPI, Form ,File, UploadFile
from fastapi.responses import FileResponse
from typing import List
from PIL import Image
from ..yolov5 import yoloAnalitics as yolo
import torch
import io
import json
import os
import shutil
from datetime import datetime
from fastapi import APIRouter
from ..utills import dbUtills
from ..models import album

db='test-db'
pictureCollection="pictures"
albumCollection = "albums"

router = APIRouter(
    prefix= '/v1',
    tags = ['production']
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


# @router.post("/uploadSingleImage/")
# async def create_upload_files(file:  bytes = File(...)) :
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         images = []
#         originalPath='./DB/Images/Original'
        
#         nativeMetadata = yolo.extractNativeMetadata(file)
#         return nativeMetadata


@router.post("/uploadPicturToAlbumAndShowResult")
async def Upload_picture_to_album_and_show_results(albumName: str , file:  UploadFile = File(...) ):
    albumId = dbUtills.QuaryObjectId(db,albumCollection,{"name":f"{albumName}"})
    if not file:
            return {"message": "No upload file sent"}
    else:
        tagCollection = "tags"
        originalPath='./DB/Images/Original'
        processedPath='./DB/Images/processed'
        originalName = file.filename
        timeNow= datetime.now()
        timeStamp = str(int(round(timeNow.timestamp())))
        newFileName= timeStamp+'_'+file.filename
        OPath = os.path.join(originalPath,newFileName)
        DPath = os.path.join(processedPath,newFileName)
        with open(OPath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        nativeMetadata = yolo.extractNativeMetadata(OPath)
        with open(OPath, "rb") as image:
            f = image.read()
            b = bytearray(f)
        input_image =Image.open(io.BytesIO(b)).convert("RGB")
        analiticsMetadata = yolo.DetectByImageReturnClassOnly(input_image)
        yolo.saveProcessedImage(input_image,DPath)
        document=dict()
        document={
            "name":originalName,
            "albume":[albumId],
            "originalPictureUri":OPath,
            "proccessedPictureUri":f"{DPath}/image0.jpg",
            "nativeMetadata": nativeMetadata,
            "analiticsMetadata":analiticsMetadata,
            "isDeleted":False
        }
        pictureId = dbUtills.InsertDocument(db,pictureCollection,document)
        dbUtills.AddPictureIdToAlbum(db,albumCollection, albumId, pictureId)
        dbUtills.AddTagsFromPicture(db,pictureCollection,tagCollection,pictureId)
        return FileResponse(f"{DPath}/image0.jpg")












