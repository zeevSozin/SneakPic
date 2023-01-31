from .DbClient import DbClient

class MongoUtills:
    def __init__(self, i_connection_string):
        self.m_connection_string = i_connection_string
        self.m_db_name = "data"
        self.m_album_name = "albums"
        self.m_pictures_name = "pictures"
        self.m_tags_name = "tags"

    def init_db(self):
        db_client = DbClient(self.m_connection_string)
        tag_collection = db_client.FindAllDocuments(self.m_db_name, self.m_tags_name)
        tag_collection_list = list()
        for item in tag_collection:
            tag_collection_list.append(item)
        if len(tag_collection_list) == 0:

            doc = {
            "tags":[

                ]
            }

            db_client.InsertDocument(self.m_db_name, self.m_tags_name, doc)

    def set_db(self, i_db_name):
        self.m_db_name = i_db_name

    
