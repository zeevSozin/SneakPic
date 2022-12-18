from fastapi import FastAPI, Form ,File, UploadFile
from typing import List
from PIL import Image
import uvicorn
from .yolov5 import yoloAnalitics as yolo
import torch
import io
import json
import os
import shutil
from datetime import datetime
import time
from .router import test_router
from .router import v1_router

app = FastAPI()

app.include_router(test_router.router)
app.include_router(v1_router.router)
new_line = '\n'
@app.get("/")
async def get_root():
    return "Hello This Api allow you to upload image and recive cobjects detected from the picture using the YOLOv5 AI algorithem, feel free to test in on [this-uri]:8080/docs"





# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8080, log_level="info")