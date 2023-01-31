from .modelBase import modelBase
from .picture import Picture
import json



def result_extractor(payload):
    content = payload.content
    jsonData = json.loads(content)
    return jsonData["resulte"]
class Tags(modelBase):

    def __init__(self, endpointUri, base_route):
        self.names = list()
        self.picture_ids = list()
        self.Pictures = list()
        self.endpointURI = endpointUri
        self.base_route = base_route
        self.get_tags_from_db()

    def Set_db_connection(self, endpointUri, base_route):
        self.endpointURI = endpointUri
        self.base_route = base_route

    def get_tags_from_db(self):
        responce = self.get("GetAlltags")
        for tag in responce:
            self.names.append(tag)

    def get_tag_list(self):
        return self.names

    def get_picture_Ids_by_filter(self, filters):
        payload= {
        "filter_list": filters
        }

        res = self.post("GetPictureIdsByFilter", payload)
        json_res = json.loads(res.content)
        agg_list = self.AggrigateList(json_res["resulte"])
        return agg_list


    def AggrigateList(self, i_list):
        master_list = list()
        sub_list =list()
        for lst in i_list:
            sub_list.append(lst)
            for l in sub_list:
                for t in l:
                    if t not in master_list:
                        master_list.append(t)   
        return master_list

    def get_pictures_by_filter(self, filters):
        self.picture_ids = self.get_picture_Ids_by_filter(filters)
        self.set_original_and_processed_pictures()
        return self.Pictures


    def set_original_and_processed_pictures(self):
        for pic_id in self.picture_ids:
            pic_name = self.get_Photo_name(pic_id)
            pic_original_photo = self.get_original_photo(pic_id)
            pic_processed_photo = self.get_processed_photo(pic_id)
            pic_metadata = self.get_photo_metadata(pic_id)
            picture = Picture(pic_name, pic_original_photo, pic_processed_photo, pic_metadata)
            self.Pictures.append(picture)

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
