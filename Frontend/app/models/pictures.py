from .modelBase import modelBase
from .picture import Picture
import json



def result_extractor(payload):
    content = payload.content
    jsonData = json.loads(content)
    return jsonData["resulte"]
class Pictures(modelBase):

    def __init__(self, endpointUri, base_route):
        self.picture_ids = list()
        self.Picture_list = list()
        self.endpointURI = endpointUri
        self.base_route = base_route
        self.get_all_picture_isd_from_db()

    def Set_db_connection(self, endpointUri, base_route):
        self.endpointURI = endpointUri
        self.base_route = base_route

    def get_all_picture_isd_from_db(self):
        res = self.get("GetAllPicturesIDs")
        data = res["resulte"]
        self.picture_ids = data

    def get_all_pictures(self):
        self.set_original_and_processed_pictures()
        return self.Picture_list
        


    def set_original_and_processed_pictures(self):
        for pic_id in self.picture_ids:
            pic_name = self.get_Photo_name(pic_id)
            pic_original_photo = self.get_original_photo(pic_id)
            pic_processed_photo = self.get_processed_photo(pic_id)
            pic_metadata = self.get_photo_metadata(pic_id)
            picture = Picture(pic_name, pic_original_photo, pic_processed_photo, pic_metadata)
            self.Picture_list.append(picture)

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
