from unittest import TestCase
from .utills import dbUtills

"""
the unit tests are testing functionality with DB , in order to perform those tests
Db should be attached!!!

"""

# class dbUtillsTest(TestCase):
#     def test_insert_document_to_collection(self):
#         document= {
#   "name": "test-album-4",
#   "description": "string",
#   "count": 0,
#   "picturs": [
    
#   ],
#   "isDeleted": False
# }
#         res = dbUtills.InsertDocument("test-db","albums",document)
#         print(res)
#         assert res == 0



    # def test_get_pictures_from_album(self):
    #     pictures = dbUtills.GetAllPicturesIdfromAlbum("test-db","albums","639cd19e9c55e30e34fd4043")
    #     print(pictures)
    #     assert pictures.count == 0



    # def test_Get_album_count(self):
    #     assert dbUtills.QuaryPicruCountFromAlbum("test-db","albums","639cd19e9c55e30e34fd4043") == 0

    #     dbUtills.UpdateAlbumCount("test-db", "albums", "639cd19e9c55e30e34fd4043", 1)

    #     assert dbUtills.QuaryPicruCountFromAlbum("test-db","albums","639cd19e9c55e30e34fd4043") == 1

    #     dbUtills.UpdateAlbumCount("test-db", "albums", "639cd19e9c55e30e34fd4043", 0)



    # def test_Get_all_albums(self):
    #     res = dbUtills.GetAllNames("test-db","albums")
    #     print(res)
    #     assert res == '["test album", "test album", "test album", "test_album_1"]'

    # def test_Get_all_pictures_and_their_album_id(self):
    #     res = dbUtills.GetAllPictureNamesAndTheirAlbumId("test-db","pictures")
    #     assert res.count == 4

    # def test_add_picture_to_album(self):
    #     albumId = "639cd19e9c55e30e34fd4043"
    #     pictureId = "639db3a365e7dd67b3da43e5"
    #     res1 = dbUtills.AddPictureIdToAlbum("test-db","albums",albumId,pictureId)
    #     res2 = dbUtills.AddAlbumtoPicture("test-db","pictures",pictureId,albumId)
        
    #     assert res1 == res2

    # def test_get_all_tags(self):
    #     res = dbUtills.GetAllTags("test-db","tags")
    #     print(res)
    #     assert res.count == 2

    # def test_get_NativeMetadata(self):
    #     res = dbUtills.GetNativeMetadatTagsfromPic("test-db","pictures","639cdab574e899374945881f")
    #     print(res)
    #     assert res.count == 9

    # def test_get_AnaliticsMetadata(self):
    #     res = dbUtills.GetAnaliticsMetadatTagsfromPic("test-db","pictures","639cdab574e899374945881f")
    #     print(res)
    #     assert res == ['car', 'bus']

    # def test_add_tag(self):
    #     dbUtills.AddTag("test-db","tags","testTag")

    # def test_add_picutre_to_tag(self):
    #     dbUtills.AddPictureIdToTag("test-db","tags","testTag","12354",55)

    # def test_get_metadata_dict(self):
    #     res = dbUtills.GetAnaliticsMetadatfromPic("test-db","pictures","639cdab574e899374945881f")
    #     assert res == 0

    # def test_tag_update_with_picture(self):
    #     res = dbUtills.AddTagsFromPicture("test-db","pictures","tags","639db2fba8dbb7fe777475c0")
    #     assert res == 0
