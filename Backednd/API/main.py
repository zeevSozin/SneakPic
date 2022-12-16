from fastapi import FastAPI, Form ,File, UploadFile
from typing import List
from PIL import Image
import uvicorn
from yolov5 import yoloAnalitics as yolo
import torch
import io
import json


app = FastAPI()
@app.get("/")
async def get_root():
    return {"message": "Hello World, This Api allow you to upload photos and recive cobject detyected from the photu using the YOLO 3 algrithem", "method": "GET"}

@app.post("/v1/getMetadataSinleImage/")
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

@app.post("/v1/getMetadaMultipleImages/")
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




@app.post("/v1/printDetectedSinleImage/")
async def create_upload_file(file: bytes = File(...)) :
    if not file:
        return {"message": "No upload file sent"}
    else:
        images = []
        input_image =Image.open(io.BytesIO(file)).convert("RGB")
        images.append(input_image)
        imageWithOverlay = yolo.PrintDetectedImage(images)
        
        return imageWithOverlay.show()




if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info")