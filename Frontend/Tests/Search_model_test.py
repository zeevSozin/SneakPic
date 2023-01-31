from unittest import TestCase
import requests
from app.models import tags, pictures, album, album_content
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

single_filter = ["person"]
filters = ["person", "boat"]


class tags_content_test(TestCase):
    def _test_getall_tags(self):
        tag_prototype = tags.Tags(endpointUri, base_route)
        res =  tag_prototype.get_tags_from_db()
        print(res)
        assert res == 0

    def _test_taglit_tags(self):
        tag_prototype = tags.Tags(endpointUri, base_route)
        res =  tag_prototype.get_tag_list()

        print(res)
        assert res == 0

    def _test_get_pictures_by_filter(self):
        tag_prototype = tags.Tags(endpointUri, base_route)
        res =  tag_prototype.get_picture_Ids_by_filter(filters)
        print(res)
        assert res == 0

    def test_get_all_picture_ids(self):
        pictures_prototype = pictures.Pictures(endpointUri, base_route)
        res = pictures_prototype.get_all_picture_isd_from_db()
        print(res)
        print(type(res))

        assert res == 0