from pymongo import MongoClient
#from ..models import album,picture

#client = MongoClient("mongodb://localhost:27017/")

def connectToDb():
    return MongoClient("mongodb://localhost:27017/")

def InsertDocument(db ,collection, document):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection] 
    mycol.insert_one(document)
    
def InsertDocuments(db, collection, documents):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection] 
    mycol.insert_many(documents)

def FindTopDocuments(db, collection):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    return mycol.find_one()

def FindAllDocuments(db, collection):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    return mycol.find()
def QuaryInCollection(db, collection, quary):
    client=connectToDb()
    mydb = client[db]
    mycol = mydb[collection]
    return mycol.find(quary)


# mydb = client["test-db"]

# collection_album = mydb["albums"]

# collection_picture = mydb["pictures"]


# doc = {
#     "name": "test album",
#     "description": " terst description",  
#     "count": 1,
#     "picturs": "",
#     "isDeleted": False
# }

# InsertDocument("test-db","albums",doc)

