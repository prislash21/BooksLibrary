import json

import pymongo
from flask import Flask
from flask import Response, request

app = Flask(__name__)
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


###########################################
@app.route('/user/signUp', methods=['POST'])
def user_signup():
    try:
        userDetails = request.get_json()
        dbResponse = db.users.insert_one(userDetails)

        return Response(
            response=json.dumps(
                {"user": "User created Successfully",
                 "userid": f"{dbResponse.inserted_id}"
                 }
            ),
            status=201,
            mimetype='application/json'
        )

    except Exception as ex:
        print('*********************')

        print("ex")
        print('********************')


###########################################


if __name__ == "__main__":
    app.run()
