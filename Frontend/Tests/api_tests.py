from unittest import TestCase
import requests
from app.models import tags, picture, album, collection
from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini")

endpointParams = config["endpoint"]
Host = endpointParams["host"]
Port = endpointParams["port"]
baseRoute = endpointParams["baseroute"]
endpointUri = Host + ":" + Port 

base_route = "v1"


class tags_test(TestCase):
    def test_get_all_tags(self):
        m_tags = tags.tags(endpointUri, "v1")
        m_tags.get_tags_from_db()
        tagList = m_tags.get_tag_list()
        print(tagList)

        assert tagList != None

    def test_ad_album(self):
        m_api_album = album.Albums(endpointUri, "v1")
        res = m_api_album.Add_album("test_album_1", "created by test")
        print(res)
        assert res == 200




