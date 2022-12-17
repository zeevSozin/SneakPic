from fastapi import FastAPI, Form ,File, UploadFile
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
from router import test_router
from router import v1_router

app = FastAPI()

app.include_router(test_router.router)
app.include_router(v1_router.router)

@app.get("/")
async def get_root():
    return {"message": "Hello World, This Api allow you to upload photos and recive cobject detyected from the photu using the YOLO 3 algrithem", "method": "GET"}





if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info")