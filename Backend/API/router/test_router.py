from fastapi import File
from typing import List
from PIL import Image
from ..yolov5 import yoloAnalitics as yolo
from bson.objectid import ObjectId
import io
import os
import json
from datetime import datetime
from fastapi import APIRouter
from ..utills import DbClient
from ..utills import mongoUtills
from ..models import api_models
import base64
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini') 
mongoParams = config["mongodb"]

mongoHost = mongoParams["host"]
mongoPort = mongoParams["port"]

connection_string = "mongodb://" + mongoHost + ":" + mongoPort

db='test-db'
pictureCollection="pictures"
albumCollection = "albums"
tagCollection = "tags"

def jsonDecorate(payload):
    decorator = {
        "resulte": payload
    }
    return decorator


router = APIRouter(
    prefix= '/v1/test',
    tags = ['testing']
)


@router.get('/')
async def init_test_database():
    mongo_client = mongoUtills.MongoUtills(connection_string)
    mongo_client.set_db(db)
    mongo_client.init_db()
    
    db_client = DbClient.DbClient(connection_string)
    db_parser = db_client.GetCollections(db)
    
    parsed_items = list()
    for item in db_parser:
        parsed_items.append(item)
    if len(parsed_items) == 1:
        json_result = json.dumps(parsed_items)
        return {"message": "Sucsessfuly initialized "+db,
        "resutl": json_result 
        }
    else:
        return {"error message": "did not initialized "+db}


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
        return detectionInfo
        

@router.post("/addAlbum")
async def create_new_album_on_DB(input_data: api_models.album):
   document=dict()
   document = {
        "name" : input_data.name,
        "description" :input_data.description,
        "count":0,
        "pictures":[],
        "isDeleted":False,
   }
   db_client = DbClient.DbClient(connection_string)
   db_client.InsertDocument(db,albumCollection,document)

@router.post("/delete_album")
async def delete_album(input_data: api_models.albumName):
    db_client = DbClient.DbClient(connection_string)
    res = db_client.QuaryObjectIdByName(db,albumCollection,input_data.album_name)
    db_client.DeleteObjectById(db, albumCollection, res)
    return {"message": "album "+input_data.album_name+" was deleted" + res}


'''
### Pictures

'''

@router.post('/UploadImageToDB')
async def create_upload_files(album_name:str, file_name: str ,file: List[bytes] = File()) :
    db_client = DbClient.DbClient(connection_string)
    albumId = db_client.QuaryObjectIdByName(db,albumCollection, album_name)
    if not file:
        return {"message": "No upload file sent"}
    else:
        tagCollection = "tags"
        processedPath='./DB/Images/processed'
        timeNow= datetime.now()
        timeStamp = str(int(round(timeNow.timestamp())))
        newFileName= timeStamp + '_' + file_name
        DPath = os.path.join(processedPath,newFileName)
        images = []
        for image in file:
            input_image =Image.open(io.BytesIO(image)).convert("RGB")
            images.append(input_image)

        base64_originalImage = base64.b64encode(image)
        base64_OriginalMessage = base64_originalImage.decode('utf-8')
        detectionInfo = yolo.DetectByImagesClassOnly(images)
        yolo.saveProcessedImage(input_image,DPath)
        with open(f"{DPath}/image0.jpg", "rb") as buffer:
            binary_data = buffer.read()
            bitArray = bytearray(binary_data)
            base64_processedImage = base64.b64encode(bitArray)
            base64_ProcessedMessage = base64_processedImage.decode('utf-8')
            document=dict()
            document={
                "name": file_name,
                "albume":[albumId],
                "originalPictureUri":base64_OriginalMessage,
                "proccessedPictureUri":base64_ProcessedMessage,
                "analiticsMetadata":detectionInfo,
                "isDeleted":False
            }
            pictureId = db_client.InsertDocument(db,pictureCollection,document)
            db_client.AddPictureIdToAlbum(db,albumCollection, albumId, pictureId)
            db_client.AddTagsFromPicture(db,pictureCollection,tagCollection,pictureId)
            os.remove(f"{DPath}/image0.jpg") ### file cleanup
            os.removedirs(DPath)### cleanup temp dir
            



@router.post("/deletePictureFromAlbum")
async def delete_picture_from_album(pic_in_album :api_models.picture_in_album ):
    db_client = DbClient.DbClient(connection_string)
    picture_id = db_client.QuaryObjectIdByName(db, pictureCollection, pic_in_album.picture_name)
    album_id = db_client.QuaryObjectIdByName(db, albumCollection, pic_in_album.album_name)
    db_client.DeletePictureFromTags(db, tagCollection, picture_id)
    db_client.DeletePictureFromAlbum(db ,albumCollection, album_id,picture_id )
    db_client.DeleteObjectById(db, pictureCollection, picture_id)


@router.post("/getPitcureIdsFromAlbum")
async def get_pictures_from_album(album_name : api_models.albumName):
    db_client = DbClient.DbClient(connection_string)
    album_id = db_client.QuaryObjectIdByName(db, albumCollection, album_name.album_name)
    res = db_client.GetAllPicturesIdfromAlbum(db , albumCollection, album_id)
    return json.loads(res)



@router.post("/getPictureName")
async def get_picture_name_by_id( picture_id: api_models.picture_id):
    db_client = DbClient.DbClient(connection_string)
    res = db_client.GetPictureNameByID(db, pictureCollection, ObjectId(picture_id.picture_id))
    json_res = jsonDecorate(res)
    return json_res



@router.post("/getOriginalPicture")
async def get_original_picture_by_id( picture_id: api_models.picture_id):
    db_client = DbClient.DbClient(connection_string)
    res = db_client.GetOriginalPicurePathFromPicture(db, pictureCollection, ObjectId(picture_id.picture_id))
    json_res = jsonDecorate(res)
    return json_res





@router.post("/getProccessedPicture")
async def get_processed_picture_by_id( picture_id: api_models.picture_id):
    db_client = DbClient.DbClient(connection_string)
    res = db_client.GetProccessedPicurePathFromPicture(db, pictureCollection, ObjectId(picture_id.picture_id))
    json_res = jsonDecorate(res)
    return json_res


@router.post("/getPictureMetadata")
async def get_picture_metadata_by_id( picture_id: api_models.picture_id):
    db_client = DbClient.DbClient(connection_string)
    res = db_client.GetPictureMetadataById(db, pictureCollection, ObjectId(picture_id.picture_id))
    json_dump = json.dumps(res)
    json_res = jsonDecorate(json_dump)
    return json_res



@router.get("/GetAllPicturesIDs")
async def get_all_picture_ids():
   db_client = DbClient.DbClient(connection_string) 
   res = db_client.GetAllPicturesIds(db, pictureCollection)
   json_res = json.loads(res)
   return jsonDecorate(json_res)

@router.get("/GetAllAlbumIDs")
async def get_all_album_ids():
   db_client = DbClient.DbClient(connection_string) 
   res = db_client.GetAllPicturesIds(db, albumCollection)
   return json.loads(res)



@router.post("/GetalbumMetadataByID")  ###  album metadata consists of : name, description and picture count
async def get_album_meta_data( albumId : api_models.albumId):
    db_client = DbClient.DbClient(connection_string) 
    res = db_client.GetAlbumMetadata(db, albumCollection, albumId.album_id)
    return res




@router.get("/GetAlltags")
async def get_all_album_ids():
   db_client = DbClient.DbClient(connection_string) 
   res = db_client.GetAllTags(db, tagCollection)
   return res



@router.post("/GetPictureIdsByFilter")
async def get_picture_ids_by_filter(filters : api_models.filters):
    db_client = DbClient.DbClient(connection_string)
    tag_list = db_client.GetAllTags(db, tagCollection)
    result_list = list()
    for tag in tag_list:
        if tag in filters.filter_list:
            res = db_client.GetAllPicturesFromTagByTagName(db, tagCollection, tag)
            result_list.append(res)
    return jsonDecorate(result_list)

