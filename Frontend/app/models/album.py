import json
from .modelBase import modelBase


class Album_obj(modelBase):
    def __init__(self, endpointUri, base_route, id):
        self.endpointURI = endpointUri
        self.base_route = base_route
        self.id = id
        

    def set_metadata_from_db(self):
        payload = {
            "album_id": f"{self.id}"
        }
        responce = self.post("GetalbumMetadataByID",payload)
        json_dict = json.loads(responce.content)
        self.name = json_dict["name"]
        self.description =json_dict["description"]
        self.count = json_dict["count"]

    def Set_db_connection(self, endpointUri, base_route):
        self.endpointURI = endpointUri
        self.base_route = base_route

    def Get_id(self):
        return self.id

    def Get_name(self):
        return self.name

    def Get_description(self):
        return self.description

    def Get_count(self):
        return self.count

class Albums(modelBase):
    def __init__(self, endpointUri, base_route):
        self.album_ids = list()
        self.albumList = list()
        self.endpointURI = endpointUri
        self.base_route = base_route
        self.albumList = self.get_album_collection()

    def Set_db_connection(self, endpointUri, base_route):
        self.endpointURI = endpointUri
        self.base_route = base_route


    def set_album_ids_from_db(self):
        responce = self.get("GetAllAlbumIDs")
        for id in responce:
            self.album_ids.append(id)

    def set_album_dict(self):
        self.set_album_ids_from_db()
        for albumId in self.album_ids:
            album = Album_obj(self.endpointURI, self.base_route, albumId)
            album.set_metadata_from_db()
            albumDict = dict()
            albumDict["id"] = album.Get_id()
            albumDict["name"] = album.Get_name()
            albumDict["description"] = album.Get_description()
            albumDict["count"] = album.Get_count()
            self.albumList.append(albumDict)

    def get_album_collection(self):
        if len(self.album_ids) == 0:
            self.set_album_dict()
        return self.albumList


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