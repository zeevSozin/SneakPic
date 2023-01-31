from unittest import TestCase
from API.utills import mongoUtills, DbClient
from API.yolov5 import yoloAnalitics as yolo
from API.router import v1_router
import base64
from fastapi import UploadFile
import json
from API.models import api_models
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini') 
mongoParams = config["mongodb"]

mongoHost = mongoParams["host"]
mongoPort = mongoParams["port"]

m_connection_string = "mongodb://" + mongoHost + ":" + mongoPort


test_db = "test_db"
db = "data"
album_collecttion = "albums"
picture_collection = "pictures"
tag_collection = "tags"

class mongo_db_test(TestCase):

    # def test_check_if_tag_exsists(self):
    #     mongo_client = mongoUtills.MongoUtills(m_connection_string)
    #     db_name = mongo_client.m_db_name
    #     print(db_name)
    #     tag_collection_name = mongo_client.m_tags_name
    #     print(tag_collection_name)
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.FindAllDocuments(db_name, tag_collection_name)
    #     parsedItems = list()
    #     for item in res:
    #         parsedItems.append(item)
    #     print (parsedItems)
    #     print(len(parsedItems))
    #     assert len(parsedItems) == 1


    # def insert_new_album(self):
    #     document=dict()
    #     document = {
    #             "name" : "testing_album_name",
    #             "description" :"testing_album_name",
    #             "count":0,
    #             "picturs":[],
    #             "isDeleted":False,
    #     }
    #     db_client = DbClient.DbClient(m_connection_string)
    #     db_client.InsertDocument(db,album_collecttion,document)

    # def delete_album(self, album_name):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     db_client.DeleteObjectById(db_client.QuaryObjectIdByName(album_name))

  

    # def test_find_album_by_name(self):
    #     self.insert_new_album()
    #     db_client = DbClient.DbClient(m_connection_string)
    #     object_id = db_client.QuaryObjectIdByName(db, album_collecttion,"testing_album_name")
    #     print(object_id)
    #     db_client.DeleteObjectById(db, album_collecttion, object_id)

    #     assert len(object_id) == 24

    # def test_DeletePictureFromAlbum(self):
    #     res =1 
    #     db_client = DbClient.DbClient(m_connection_string)
    #     db_client.DeletePictureFromAlbum(db, album_collecttion, "63ca9812a4df921317725c3a", "63cbbfd7118630af7acc27c3")

    #     assert res == 0

    # def test_delete_picture_from_album(self):
    #     res =1

    #     json_payload = {"album_name":"album_1",
    #     "picture_name": "traffic.jpg"}
    #     payload = api_models.picture_in_album(**json_payload)

    #     db_client = DbClient.DbClient(m_connection_string)
    #     picture_id = db_client.QuaryObjectIdByName(db, picture_collection, payload.picture_name)
    #     album_id = db_client.QuaryObjectIdByName(db, album_collecttion, payload.album_name)
    #     pictures = db_client.GetAllPicturesIdfromAlbum(db, album_collecttion, album_id)
    #     pic_list = list()
    #     pics_json = json.loads(pictures)
    #     for pic in pics_json:
    #         pic_list.append(pic)
    #         print(pic)
    #     print(pic_list)

    #     assert res == 0


    # def test_get_all_tags(self):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res =db_client.GetAllTags(db,tag_collection)
    #     print(res)
    #     assert len(res) != 0

    # def test_get_tag_record_id(self):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.GetTagsRecordId(db, tag_collection)
    #     print(res)
    #     assert len(res) == 24

    # def test_GetAllPicturesFromTagByTagName(self):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.GetAllPicturesFromTagByTagName(db,tag_collection,"car")
    #     print(res)
    #     assert res != 0

    # def test_DeletePictureFromTags(self):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.DeletePictureFromTags(db, tag_collection, "63cbbfd7118630af7acc27c3")
    #     assert res == None

    # def test_GetOriginalPicurePathFromPicture(self):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.GetOriginalPicurePathFromPicture(db, picture_collection, "63cbbfd7118630af7acc27c3")
    #     print(res)
    #     assert res != None

    # def test_get_pictures_from_album(self):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     album_id = db_client.QuaryObjectIdByName(db, album_collecttion, "album_1")
    #     res =db_client.GetAllPicturesIdfromAlbum(db , album_collecttion, album_id)
    #     print(res)
    #     assert res == 0

    # def test_QuaryObjectIdByName(self):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.QuaryObjectIdByName(db, picture_collection, "traffic.jpg")
    #     print(res)

    #     assert res == 0


    # def test_get_tags(self):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.FindAllDocuments("data", "tags")
    #     print(res)
    #     assert res == 0

    # def test_get_all_collections(self):
    #     db_client = DbClient.DbClient(m_connection_string)
    #     collections = db_client.GetCollections("data")
    #     print(collections)

    #     assert collections == 0

    # def test_CheckIfPictureCollectionInTagIsEmpty(self):
    #     res =1
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.CheckIfPictureCollectionInTagIsEmpty(db,tag_collection, "car")
    #     print (res)
    #     assert res == 0


    # def test_DeleteEmptyTag(self):
    #     res =1
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.DeleteEmptyTag(db,tag_collection, "car")
    #     print (res)
    #     assert res == 0

    # def test_GetAllPicturesIdfromAlbum(self):
    #     res =1
    #     db_client = DbClient.DbClient(m_connection_string)
    #     res = db_client.GetAllPicturesIdfromAlbum(db,album_collecttion, "63d984ea7543ddeba5847068")
    #     print (res)
    #     print (type(res))
    #     json_picture = json.loads(res)
    #     print(json_picture)
    #     print(type(json_picture))

    #     assert res == 0

    

    
        




        
