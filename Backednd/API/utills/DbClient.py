from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import json


class DbClient:
    def __init__(self,i_connection_string):
        self.m_connection_string = i_connection_string

    def connectToDb(self):
        return MongoClient(self.m_connection_string)

    def GetCollections(self, db):
        client = self.connectToDb()
        mydb = client[db]
        collections = mydb.list_collection_names()
        return collections

    def InsertDocument(self, db, collection, document):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        res = mycol.insert_one(document)
        objId = res.inserted_id
        return str(objId)

    def InsertDocuments(self, db, collection, documents):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        mycol.insert_many(documents)

    def FindTopDocuments(self, db, collection):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        return mycol.find_one()

    def FindAllDocuments(self, db, collection):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        return mycol.find()

    def QuaryObjectIdByName(self, db, collection, name):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        cursor = mycol.find_one({"name": name})
        if not (cursor):
            print("No object where found")
            return "No object where found"
        else:
            return str(cursor['_id'])

    # def QuaryObjectsIdByName(self, db, collection, name):
    #     client = self.connectToDb()
    #     mydb = client[db]
    #     mycol = mydb[collection]
    #     cursor = mycol.find({"name": name})
    #     if not (cursor):
    #         print("No object where found")
    #         return "No object where found"
    #     else:
    #         return str(cursor['_id'])

    def QuaryInCollection(self, db, collection, quary):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        cursor = mycol.find(quary)
        # list_cur = list(cursor)
        # json_data = dumps(list_cur)
        # json_data_1 = json.load(json_data)
        # objectId = json_data_1['_id']
    # return objectId

    def QuaryPictureCountFromAlbum(self, db, collection, albumId):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        cursor = mycol.find_one({"_id": ObjectId(albumId)})
        if not (cursor):
            print("No object where found")
            return "No object where found"
        else:
            return int(cursor['count'])

    def GetAlbumMetadata(self, db, albumcollection, albumId):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[albumcollection]
        cursor = mycol.find_one({"_id": ObjectId(albumId)})
        album_name = cursor["name"]
        album_description = cursor["description"]
        album_count = cursor["count"]
        return {
            "name": album_name,
            "description": album_description,
            "count": album_count
        }


    def UpdateAlbumCount(self, db, collection, albumId, count):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        mycol.update_one({"_id": ObjectId(albumId)},
                         {"$set": {"count": count}})

    def GetAllNames(self, db, collection):
        cursor = self.FindAllDocuments(db, collection)
        albumNames = list()
        for obj in cursor:
            albumNames.append(obj["name"])
        return json.dumps(albumNames)

    def GetAllPicturesIds(self, db, pictureCollection):
        cursor = self.FindAllDocuments(db, pictureCollection)
        mydict = {}
        myList = list()
        for obj in cursor:
            objectContainer = obj["_id"]
            val = str(objectContainer)
            myList.append(val)
        return json.dumps(myList)
        

    def GetAllPictureNamesAndTheirAlbumId(self, db, collection):
        cursor = self.FindAllDocuments(db, collection)
        mydict = {}
        for obj in cursor:
            mydict[obj["name"]] = obj["album"]
        return json.dumps(mydict)

    def GetAllPicturesIdfromAlbum(self, db, collection, albumId):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        album = mycol.find_one({"_id": ObjectId(albumId)})
        pictires = album["pictures"]
        return json.dumps(pictires)

    def AddPictureIdToAlbum(self, db, collection, albumId, pictureId):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        res = mycol.update_one({"_id": ObjectId(albumId)}, {
                               "$push": {"pictures": pictureId}, "$inc": {"count": 1}})
        return res

    def AddAlbumtoPicture(self, db, collection, pictureId, albumId):
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        res = mycol.update_one({"_id": ObjectId(pictureId)}, {
                               "$push": {"album": albumId}})
        return res

    def GetAllTags(self, db, collection):
        cursor = self.FindTopDocuments(db, collection)
        tagList = list()
        tags = list()
        tagList.append(list(cursor["tags"]))
        for tag in tagList:
            for t in tag:
                tagDict = dict(t)
                tags.append(tagDict["name"])
        return tags

    def GetNativeMetadatTagsfromPic(self, db, collection, pictureId):
        client = self.connectToDb()
        mydb = client[db]
        pictureCollection = mydb[collection]
        Pcursor = pictureCollection.find_one({"_id": ObjectId(pictureId)})
        nativeDict = dict(Pcursor["nativeMetadata"])
        nativeList = list(nativeDict.keys())
        return nativeList

    def GetAnaliticsMetadatfromPic(self, db, collection, pictureId):
        client = self.connectToDb()
        mydb = client[db]
        pictureCollection = mydb[collection]
        Pcursor = pictureCollection.find_one({"_id": ObjectId(pictureId)})
        nativeDict = dict(Pcursor["analiticsMetadata"])
        return nativeDict

    def GetAnaliticsMetadatTagsfromPic(self, db, collection, pictureId):
        client = self.connectToDb()
        mydb = client[db]
        pictureCollection = mydb[collection]
        Pcursor = pictureCollection.find_one({"_id": ObjectId(pictureId)})
        nativeDict = dict(Pcursor["analiticsMetadata"])
        nativeList = list(nativeDict.keys())
        return nativeList

    def AddTag(self, db, collection, tag):
        cursor = self.FindTopDocuments(db, collection)
        objectId = cursor["_id"]
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        mycol.update_one({"_id": ObjectId(objectId)}, {
                         "$push": {"tags": {"name": f"{tag}", "pictures": []}}})

    def AddPictureIdToTag(self, db, collection, tag, pictureId, count):
        cursor = self.FindTopDocuments(db, collection)
        objectId = cursor["_id"]
        client = self.connectToDb()
        mydb = client[db]
        mycol = mydb[collection]
        mycol.update_one({"_id": ObjectId(objectId), "tags.name": f"{tag}"}, {
                         "$push": {f"tags.$.pictures": {"pictureId": f"{pictureId}", "count": count}}})

    def AppendTagsToCollection(self, db, collection, additionalTagList):
        originalTagList = self.GetAllTags(db, collection)
        for tag in additionalTagList:
            if (tag not in originalTagList):
                self.AddTag(db, collection, tag)

    def AddTagsFromPicture(self, db, pictureCollection, tagCollection, pictureId):
        analiticsMetadata = self.GetAnaliticsMetadatTagsfromPic(
            db, pictureCollection, pictureId)
        self.AppendTagsToCollection(db, tagCollection, analiticsMetadata)
        tagDict = self.GetAnaliticsMetadatfromPic(db, pictureCollection, pictureId)
        for tag in list(tagDict.keys()):
            self.AddPictureIdToTag(db, tagCollection, tag, pictureId, tagDict[tag])

    def DeleteObjectById(self, db, collection, object_id):
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[collection]

        my_collection.delete_one({"_id": ObjectId(object_id)})

    def DeletePictureFromAlbum(self, db, albumCollection,albumId ,pic_obj_id):
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[albumCollection]
        my_collection.update_one({"_id": ObjectId(albumId)},
         {"$pull":{"pictures": f"{pic_obj_id}" }, "$inc": {"count": -1}})



    def GetTagsRecordId(self, db, tagCollection):
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[tagCollection]
        cursor = my_collection.find_one()
        return str(cursor['_id'])


    def GetAllPicturesFromTagByTagName(self, db, tagCollection, tag_name):
        tag_rec_id = self.GetTagsRecordId(db,tagCollection)
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[tagCollection]
        cursor = my_collection.find_one({"_id":ObjectId(tag_rec_id)})
        picture_rec_list = list()
        tagList = list()
        tagList.append(list(cursor["tags"]))
        for tag in tagList:
            for t in tag:
                if t["name"] == tag_name:
                    for pic in t["pictures"]:
                        picture_rec_list.append(pic["pictureId"])
        return picture_rec_list


    def DeletePictureIdFromPicturesArrayInTags(self, db, tagCollection,tagName ,picture_id):
        tag_rec_id = self.GetTagsRecordId(db,tagCollection)
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[tagCollection]
        my_collection.update_one({"_id": ObjectId(tag_rec_id), "tags.name": f"{tagName}" },
        {"$pull" : {f"tags.$.pictures": {"pictureId": f"{picture_id}" }}})
         


    def DeletePictureFromTags(self, db, tagCollection, picture_id):
        tag_rec_id = self.GetTagsRecordId(db,tagCollection)
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[tagCollection]
        cursor = my_collection.find()
        tags_list = self.GetAllTags(db,tagCollection)
        for item in tags_list:
            picture_ids_in_tag = self.GetAllPicturesFromTagByTagName(db, tagCollection, item)
            if (picture_id in picture_ids_in_tag):
                self.DeletePictureIdFromPicturesArrayInTags(db, tagCollection, item, picture_id)
        

 
    def GetOriginalPicurePathFromPicture(self, db, pictureCollection, picture_id):
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[pictureCollection]
        cursor = my_collection.find_one({"_id": ObjectId(picture_id)})
        return (str(cursor["originalPictureUri"]))


    def GetProccessedPicurePathFromPicture(self, db, pictureCollection, picture_id):
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[pictureCollection]
        cursor = my_collection.find_one({"_id": ObjectId(picture_id)})
        return (str(cursor["proccessedPictureUri"]))


    def GetPictureMetadataById(self, db, pictureCollection, picture_id):
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[pictureCollection]
        cursor = my_collection.find_one({"_id": ObjectId(picture_id)})
        return (cursor["analiticsMetadata"])
         

    def GetPictureNameByID(self, db, pictureCollection, picture_id):
        client = self.connectToDb()
        mydb = client[db]
        my_collection = mydb[pictureCollection]
        cursor = my_collection.find_one({"_id": ObjectId(picture_id)})
        return (str(cursor["name"]))

    




        
     

    # def GetAllTags(self, db, collection):
    #     cursor = self.FindTopDocuments(db, collection)
    #     tagList = list()
    #     tags = list()
    #     tagList.append(list(cursor["tags"]))
    #     for tag in tagList:
    #         for t in tag:
    #             tagDict = dict(t)
    #             tags.append(tagDict["name"])
    #     return tags










        
        


