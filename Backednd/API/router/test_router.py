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
        #json_metadata = json.loads(detectionInfo)
        return detectionInfo

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

@router.post('/UploadImageToDBAndGetImageOverlay')
async def upload_picture_to_batabase(file:  UploadFile = File(...)) :
    if not file:
        return {"message": "No upload file sent"}
    else:
        originalPath='../DB/Images/Original'
        processedPath='../DB/Images/processed'
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
            "albume":[],
            "originalPictureUri":OPath,
            "proccessedPictureUri":f"{DPath}/image0.jpg",
            "nativeMetadata": nativeMetadata,
            "analiticsMetadata":analiticsMetadata,
            "isDeleted":False
        }
        dbUtills.InsertDocument(db,pictureCollection,document)
        return FileResponse(f"{DPath}/image0.jpg")

@router.post("/addAlbum")
async def createNewAlbum(input_data: album.album):
   document=dict()
   document = {
        "name" : input_data.name,
        "description" :input_data.description,
        "count":0,
        "picturs":[],
        "isDeleted":False,
   }
   dbUtills.InsertDocument(db,albumCollection,document)

@router.get("/GetAlbumId")
async def Get_album_object_Id_by_name(albumName: str ):
    albumId = dbUtills.QuaryObjectId(db,albumCollection,{"name":f"{albumName}"})
    return albumId
@router.post("/uploadPicturToAlbumAndShowResuls")
async def Upload_picture_to_album_and_show_results(albumName: str , file:  UploadFile = File(...) ):
    albumId = dbUtills.QuaryObjectId(db,albumCollection,{"name":f"{albumName}"})
    if not file:
            return {"message": "No upload file sent"}
    else:
        originalPath='../DB/Images/Original'
        processedPath='../DB/Images/processed'
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
        return FileResponse(f"{DPath}/image0.jpg")

