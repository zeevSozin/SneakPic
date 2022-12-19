from fastapi import FastAPI, Form ,File, UploadFile
from typing import List
from .yolov5 import yoloAnalitics as yolo
from datetime import datetime
from .router import test_router
from .router import v1_router
from .utills import dbUtills

app = FastAPI()

app.include_router(test_router.router)
app.include_router(v1_router.router)
new_line = '\n'
@app.get("/")
async def get_root():
    ###          inserting tag to db              ###
    doc = {
        "tags":[

        ]
    }
    dbUtills.InsertDocument("test_db","tags",doc)
    ###          end of insert                    ###


    return "Hello This Api allow you to upload image and recive cobjects detected from the picture using the YOLOv5 AI algorithem, feel free to test in on [this-uri]:8080/docs"





# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8080, log_level="info")