from fastapi import FastAPI, Form ,File, UploadFile
from typing import List
from .yolov5 import yoloAnalitics as yolo
from datetime import datetime
from .router import test_router
from .router import v1_router
from .utills import mongoUtills
import uvicorn
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
mongoParams = config["mongodb"]

mongoHost = mongoParams["host"]
mongoPort = mongoParams["port"]

connectionString = "mongodb://" + mongoHost + ":" + mongoPort

app = FastAPI()

app.include_router(test_router.router)
app.include_router(v1_router.router)
new_line = '\n'
@app.get("/")
async def get_root():
    mongo_client = mongoUtills.MongoUtills(connectionString)
    mongo_client.init_db()



    return "Hello This Api allow you to upload image and recive cobjects detected from the picture using the YOLOv5 AI algorithem, feel free to test in on [this-uri]:8080/docs"





# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8080, log_level="info")