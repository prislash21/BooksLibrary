import pymongo




 # Connection with the database
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.bookslibrary
    mongo.server_info()
except:
    print("cannot connect to DB")