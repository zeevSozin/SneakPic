import pymongo

myclient = pymong.MongoClient("mongodb://localhost:27017/")


mydb = myclient["test-db"]

collection_album = mydb["albums"]

collection_picture = mydb["pictures"]
