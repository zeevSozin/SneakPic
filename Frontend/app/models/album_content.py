import json
from .modelBase import modelBase
from .picture import Picture
from .album import Album_obj


def result_extractor(payload):
    content = payload.content
    jsonData = json.loads(content)
    return jsonData["resulte"]

class Album(modelBase):
    def __init__(self, endpointUri, base_route, album_name):
        self.album_name = album_name
        self.pictureIds = list()
        self.Pictures = list()
        self.AlbumIds = list()
        self.albums = list()
        self.endpointURI = endpointUri
        self.base_route = base_route
        self.set_album_dict()
        self.pictureIds = self.get_picture_ids_from_album()
        self.set_original_and_processed_pictures()



    def Set_db_connection(self, endpointUri, base_route):
        self.endpointURI = endpointUri
        self.base_route = base_route

    def set_album_ids_from_db(self):
        responce = self.get("GetAllAlbumIDs")
        for id in responce:
            self.AlbumIds.append(id)

    def set_album_dict(self):
        self.set_album_ids_from_db()
        for albumId in self.AlbumIds:
            album = Album_obj(self.endpointURI, self.base_route, albumId)
            album.set_metadata_from_db()
            albumDict = dict()
            albumDict["id"] = album.Get_id()
            albumDict["name"] = album.Get_name()
            albumDict["description"] = album.Get_description()
            albumDict["count"] = album.Get_count()
            self.albums.append(albumDict)
    
    def get_album_names(self):
        album_list = list()
        for obj in self.albums:
            album_list.append(obj["name"])
        return album_list


    def get_picture_ids_from_album(self):
        payload = {
        "album_name": self.album_name
        }
        res = self.post("getPitcureIdsFromAlbum", payload)
        resList = json.loads(res.content)
        return resList
        
    def get_Photo_name(self, picture_id):
        payload = {
        "picture_id": picture_id
        }
        res = self.post("getPictureName", payload)
        return result_extractor(res)

    

    def get_original_photo(self, picture_id):
        payload = {
        "picture_id": picture_id
        }
        res = self.post("getOriginalPicture", payload)
        return result_extractor(res)


    def get_processed_photo(self, picture_id):
        payload = {
        "picture_id": picture_id
        }
        res = self.post("getProccessedPicture", payload)
        return result_extractor(res)


    def get_photo_metadata(self, picture_id):
        payload = {
        "picture_id": picture_id
        }
        res = self.post("getPictureMetadata", payload)
        return result_extractor(res)


    def set_original_and_processed_pictures(self):
        for pic_id in self.pictureIds:
            pic_name = self.get_Photo_name(pic_id)
            pic_original_photo = self.get_original_photo(pic_id)
            pic_processed_photo = self.get_processed_photo(pic_id)
            pic_metadata = self.get_photo_metadata(pic_id)
            picture = Picture(pic_name, pic_original_photo, pic_processed_photo, pic_metadata)
            self.Pictures.append(picture)


    def Get_pictures(self):
        return self.Pictures


    def Get_AlbumName(self):
        return self.album_name

    def Get_Picture_ids(self):
        return self.pictureIds

    def Get_Original_pictures(self):
        return self.original_pictures


    def Get_Processed_pictures(self):
        return self.processed_pictures

    
    def Upload_picture_to_Db(self, file_name, files):
        endpoint = "UploadImageToDB/?album_name=" + self.album_name + "&" + "file_name=" + file_name 
        result = self.postFile(endpoint,files)
        return result.status_code  

    def Set_album(self,album_name):
        self.album_name = album_name
        self.pictureIds = list()
        self.Pictures = list()
        self.pictureIds = self.get_picture_ids_from_album()
        self.set_original_and_processed_pictures()



    def Add_album(self, album_name, album_description):
        payload = {
            "name": album_name,
            "description": album_description,
            "count": 0,
            "pictures":[

            ],
            "isDeleted": "false"
        }
        res = self.post("addAlbum", payload)
        return res.status_code

    def Delete_album(self, album_name):
        payload ={
        "album_name": album_name
        } 

        self.post("delete_album", payload)

    def Delete_picture(self, picture_name):
        payload = {
        "album_name": self.album_name,
        "picture_name": picture_name
        }

        self.post("deletePictureFromAlbum", payload)
