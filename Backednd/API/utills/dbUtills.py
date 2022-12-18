from pymongo import MongoClient
from bson.objectid import ObjectId 
from bson.json_util import dumps, loads
import json
#from ..models import album,picture

#client = MongoClient("mongodb://localhost:27017/")

def connectToDb():
    return MongoClient("mongodb://DB:27017/")

def InsertDocument(db ,collection, document):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection] 
    res = mycol.insert_one(document)
    objId = res.inserted_id
    return str(objId)
    
def InsertDocuments(db, collection, documents):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection] 
    mycol.insert_many(documents)

def FindTopDocuments(db, collection):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    return mycol.find_one()

def FindAllDocuments(db, collection):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    return mycol.find()

def QuaryObjectId(db, collection, quary):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    cursor = mycol.find_one(quary)
    if not (cursor):
        print("No object where found")
        return "No object where found"
    else:
        return str(cursor['_id'])

def QuaryInCollection(db, collection, quary):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    cursor = mycol.find(quary)
    # list_cur = list(cursor)
    # json_data = dumps(list_cur)
    # json_data_1 = json.load(json_data)
    # objectId = json_data_1['_id']
   # return objectId

def QuaryPicruCountFromAlbum(db,collection,albumId):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    cursor = mycol.find_one({"_id": ObjectId(albumId)})
    if not (cursor):
        print("No object where found")
        return "No object where found"
    else:
        return int(cursor['count'])

def UpdateAlbumCount(db, collection, albumId,count):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    mycol.update_one({"_id":ObjectId(albumId)},{"$set":{"count": count}})

def GetAllNames(db,collection):
    cursor = FindAllDocuments(db, collection)
    albumNames = list()
    for obj in cursor:
        albumNames.append(obj["name"])
    return json.dumps(albumNames)

def GetAllPictureNamesAndTheirAlbumId(db,collection):
    cursor = FindAllDocuments(db, collection)
    mydict = {}
    for obj in cursor:
        mydict[obj["name"]] = obj["albume"]
    return json.dumps(mydict)

def GetAllPicturesIdfromAlbum(db,collection,albumId):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    album = mycol.find_one({"_id":ObjectId(albumId)})
    pictires = album["picturs"]
    return json.dumps(pictires)

def AddPictureIdToAlbum(db,collection,albumId,pictureId):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    res = mycol.update_one({"_id":ObjectId(albumId)},{"$push":{"picturs": pictureId},"$inc":{"count":1}})
    return res

def AddAlbumtoPicture(db,collection,pictureId,albumId):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    res = mycol.update_one({"_id":ObjectId(pictureId)},{"$push":{"albume": albumId}})
    return res  



def GetAllTags(db,collection):
    cursor = FindTopDocuments(db,collection)
    tagList = list()
    tags = list()
    tagList.append(list(cursor["tags"]))
    for tag in tagList:
        for t in tag:
            tagDict = dict(t)
            tags.append(tagDict["name"])
    return tags

def GetNativeMetadatTagsfromPic(db,collection,pictureId):
    client=connectToDb()
    mydb = client[db]
    pictureCollection = mydb[collection]
    Pcursor = pictureCollection.find_one({"_id":ObjectId(pictureId)})
    nativeDict = dict(Pcursor["nativeMetadata"])
    nativeList = list(nativeDict.keys())
    return nativeList

def GetAnaliticsMetadatfromPic(db,collection,pictureId):
    client=connectToDb()
    mydb = client[db]
    pictureCollection = mydb[collection]
    Pcursor = pictureCollection.find_one({"_id":ObjectId(pictureId)})
    nativeDict = dict(Pcursor["analiticsMetadata"])
    return nativeDict

def GetAnaliticsMetadatTagsfromPic(db,collection,pictureId):
    client=connectToDb()
    mydb = client[db]
    pictureCollection = mydb[collection]
    Pcursor = pictureCollection.find_one({"_id":ObjectId(pictureId)})
    nativeDict = dict(Pcursor["analiticsMetadata"])
    nativeList = list(nativeDict.keys())
    return nativeList


def AddTag(db,collection,tag):
    cursor = FindTopDocuments(db,collection)
    objectId = cursor["_id"]
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    mycol.update_one({"_id":ObjectId(objectId)},{"$push":{"tags": {"name":f"{tag}","pictures":[]} }})

def AddPictureIdToTag(db,collection,tag,pictureId,count):
    cursor = FindTopDocuments(db,collection)
    objectId = cursor["_id"]
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    mycol.update_one({"_id":ObjectId(objectId),"tags.name":f"{tag}"},{"$push":{f"tags.$.pictures":{"pictureId":f"{pictureId}","count":count}}})


def AppendTagsToCollection(db,collection,additionalTagList):
    originalTagList = GetAllTags(db,collection)
    for tag in additionalTagList:
        if(tag not in originalTagList):
            AddTag(db,collection,tag)


def AddTagsFromPicture(db,pictureCollection,tagCollection,pictureId):
    analiticsMetadata = GetAnaliticsMetadatTagsfromPic(db,pictureCollection,pictureId)
    AppendTagsToCollection(db,tagCollection,analiticsMetadata)
    tagDict = GetAnaliticsMetadatfromPic(db,pictureCollection,pictureId)
    for tag in list(tagDict.keys()):
        AddPictureIdToTag(db,tagCollection,tag,pictureId,tagDict[tag])

















# mydb = client["test-db"]
# collection_album = mydb["albums"]
# collection_picture = mydb["pictures"]
# doc = {
#     "name": "test album",
#     "description": " terst description",  
#     "count": 1,
#     "picturs": "",
#     "isDeleted": False
# }

# InsertDocument("test-db","albums",doc)

