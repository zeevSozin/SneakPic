from unittest import TestCase
from app.models import tags, picture, album, collection, album_content
from app.models.picture import Picture
import json
from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini")

endpointParams = config["endpoint"]
Host = endpointParams["host"]
Port = endpointParams["port"]
baseRoute = endpointParams["baseroute"]
endpointUri = Host + ":" + Port 

base_route = "v1"


### change the album name accordingly
album_name = "album_4"

def result_extractor(payload):
    jsonData = json.loads(payload)
    # data_dict = payload
    return jsonData["resulte"]

class album_content_test(TestCase):
    def _test_album_name(self):
        album_prototype = album_content.Album(endpointUri, base_route, album_name)
        res =  album_prototype.Get_AlbumName()
        print(res)
        assert res == album_name

    def _test_photos_name(self):
        res = 0
        pictures = list([Picture])
        album_prototype = album_content.Album(endpointUri, base_route, album_name)
        pictures = album_prototype.Get_pictures()
        for pic in pictures:
            data = pic.get_name()
            print(data)
        assert res != 0 

    def _test_get_original_photo(self):
        res = 0
        pictures = list([Picture])
        album_prototype = album_content.Album(endpointUri, base_route, album_name)
        pictures = album_prototype.Get_pictures()
        for pic in pictures:
            data = pic.get_Original_photo()
            print(data)
        assert res == 1 
    
    def _test_get_processed_photo(self):
        res = 0
        pictures = list([Picture])
        album_prototype = album_content.Album(endpointUri, base_route, album_name)
        pictures = album_prototype.Get_pictures()
        for pic in pictures:
            data = pic.get_Processed_photo()
            print(data)
        assert res == 1 

    def test_get_photo_metadata(self):
        res = 0
        pictures = list([Picture])
        album_prototype = album_content.Album(endpointUri, base_route, album_name)
        pictures = album_prototype.Get_pictures()
        for pic in pictures:
            data = pic.get_metadata()
            print(data)
        assert res == 1 

    def _test_get_album_nameList(self):
        res = 0
        albums = list()
        album_prototype = album_content.Album(endpointUri, base_route, album_name)
        albums = album_prototype.get_album_names()
        for obj in albums:
            data = obj
            print(data)
        assert res == 1 


    def _test_result_extractor_nameList(self):
        res = 0
        albums = list()
        album_prototype = album_content.Album(endpointUri, base_route, album_name)
        albums = album_prototype.get_album_names()
        for obj in albums:
            data = obj
            print(data)
        assert res == 1 

    


    








