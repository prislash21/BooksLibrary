from flask import Flask
from flask import Response, request
import pymongo
import json

app= Flask(__name__)
# this is the DB connection portion
try:
    mongo = pymongo.MongoClient(
       host= "localhost" ,
        port= 27017,
        serverSelectionTimeoutMS= 1000
    )
    db= mongo.bookslibrary
    mongo.server_info()
except:
    print("cannot connect to DB")

    app.run()