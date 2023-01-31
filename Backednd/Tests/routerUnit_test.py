from unittest import TestCase
from API.utills import mongoUtills, DbClient
from API.yolov5 import yoloAnalitics as yolo
from API.router import v1_router
import base64
from fastapi import UploadFile
import json
from API.models import api_models
from API.models import album

m_connection_string = "mongodb://localhost:27017"

test_db = "test_db"
db = "data"
album_collecttion = "albums"
picture_collection = "pictures"
tag_collection = "tags"

class route_v1_test(TestCase):
    def test_get_original_picture_path_by_id(self):
        db_client = DbClient.DbClient(m_connection_string)
        res = db_client.GetOriginalPicurePathFromPicture(db, picture_collection, "63cbbfd7118630af7acc27c3")
        json_res = json.dumps(res)
        print(json_res)

        assert json_res != None



    def test_get_all_picture_ids(self):
        db_client = DbClient.DbClient(m_connection_string) 
        res = db_client.GetAllPicturesIds(db, picture_collection)
        print(res)

        assert res == 0


    def test_get_picture_ids_by_filter(self):
        filters = ["car", "truck"]
        db_client = DbClient.DbClient(m_connection_string)
        tag_list = db_client.GetAllTags(db, tag_collection)
        result_list = list()
        for tag in tag_list:
            if tag in filters:
                res = db_client.GetAllPicturesFromTagByTagName(db, tag_collection, tag)
                result_list.append(res)
        json_res = json.dumps(result_list)
        print(json_res)

        assert json_res == 0

     # def test_yolo_image_to_base64(self):
    #     with open('./DB/Images/Original/skiVecation1.jpg', "rb") as img_file:
    #         my_string = base64.b64decode(img_file.read())
    #     print(my_string)
    #     assert my_string == 0
            
        

    # def test_yolo_detection(self):
    #     result = yolo.GetProcessedImage('./DB/Images/Original/traffic.jpg')
    #     print(result) 

    #     assert result == 0



    # def test_upload_picture_to_album_base64(self):
    #     test_file = './DB/Images/Original/traffic.jpg'
    #     file = open(test_file,'rb')
    #     # files = {'file': ('traffic.jpg', open(test_file, 'rb'))}

    #     test_upload_file = UploadFile('traffic.jpg',file)
    #     # test_upload_file = UploadFile(files)
    #     res = v1_router.Upload_picture_to_album_and_show_results("album_1",test_upload_file )
    #     assert res == 0





    



