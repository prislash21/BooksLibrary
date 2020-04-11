import json
from datetime import datetime
import pymongo
from bson.objectid import ObjectId
from flask import Flask
from flask import Response, request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
from kanpai import Kanpai
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'
jwt = JWTManager(app)


# Database Configuration ###
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=40000
    )
    db = mongo.bookslibrary
    mongo.server_info()
except Exception as ex:
    print(ex)


########################################

# User Controller ###########################
# User Sign Up Controller
@app.route('/user/signUp', methods=['POST'])
def user_signup():
    # User requestBody validation
    validation_result = schema.validate(request.json)
    if validation_result.get('success', False) is False:
        return Response(
            response=json.dumps(
                {"Error": validation_result.get("error")
                 }
            ),
            status=400,
            mimetype='application/json'
        )

    try:
        userDetails = request.get_json()
        dbResponse = userSignUp(userDetails)
        if dbResponse == "exists":
            return Response(
                response=json.dumps(
                    {"user": "User already exists with provided email Id"
                     }
                ),
                status=409,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps(
                    {"user": "User created Successfully"
                     }
                ),
                status=201,
                mimetype='application/json'
            )
    # For catching exception
    except Exception as ex:
        print('*********************')

        print(ex)
        print('********************')


# User SignIn Controller
@app.route('/user/signIn', methods=['POST'])
def user_signIn():
    try:
        userLogInDetails = request.get_json()
        dbResponse = signIn(userLogInDetails)
        if dbResponse.__eq__("Error"):
            return Response(
                response=json.dumps(
                    {"Error": "Failed"
                     }
                ),
                status=400,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps(
                    {"user": dbResponse
                     }
                ),
                status=201,
                mimetype='application/json'
            )
    # For catching exception
    except Exception as ex:
        print('*********************')

        print(ex)
        print('********************')


###############################################################

# Book Controller #############################################
@app.route('/book/createBook', methods=['POST'])
@jwt_required
def create_book():
    # Get user and his role from token and check  if he is authorized to do this action or not
    current_user = get_jwt_identity()
    userRoles = current_user['roles']
    if userRoles == "ADMIN":
        try:
            bookDetails = request.get_json()
            dbResponse = createBook(bookDetails)

            return Response(
                response=json.dumps(
                    {"message": "Book created Successfully",
                     "bookId": f"{dbResponse.inserted_id}"
                     }
                ),
                status=201,
                mimetype='application/json'
            )
        except Exception as ex:
            print('*********************')

            print(ex)
            print('********************')
    else:
        return Response(
            response=json.dumps(
                {"message": "User is unauthorized to create book"
                 }
            ),
            status=403,
            mimetype='application/json'
        )


@app.route('/book/bookList', methods=['GET'])
@jwt_required
def see_book_list():
    try:
        booklist = seeBookList()

        return Response(
            response=json.dumps(booklist),
            status=200,
            mimetype='application/json'
        )



    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps(
                {"message": "Booklist is not showing"}
            ),
            status=500,
            mimetype='application/json'
        )


@app.route('/book/updateBook/<id>', methods=['PATCH'])
@jwt_required
def update_book_info(id):
    # Get user and his role from token and check he is authorize to do this action or not
    current_user = get_jwt_identity()
    userRoles = current_user['roles']
    if userRoles == "ADMIN":
        try:
            dbResponse = updateBookInfo(id, request.json)

            if dbResponse.modified_count == 1:
                return Response(
                    response=json.dumps(
                        {"message": "updated Successfully! :) "}
                    ),
                    status=200,
                    mimetype='application/json'
                )
            else:
                return Response(
                    response=json.dumps(
                        {"message": "nothing to update.... :) "}
                    ),
                    status=200,
                    mimetype='application/json'
                )


        except Exception as ex:
            print("**********")
            print(ex)
            print("***********")
            return Response(
                response=json.dumps(
                    {"message": "Sorry ! :( can not update "}
                ),
                status=404,
                mimetype='application/json'
            )

    else:
        return Response(
            response=json.dumps(
                {"message": "User is unauthorized to create book"
                 }
            ),
            status=403,
            mimetype='application/json'
        )


@app.route('/book/deleteBook/<id>', methods=['DELETE'])
@jwt_required
def delete_book_info(id):
    # Get user and his role from token and check he is authorize to do this action or not
    current_user = get_jwt_identity()
    userRoles = current_user['roles']
    if userRoles == "ADMIN":
        try:
            dbResponse = deleteBookInfo(id)
            if dbResponse.deleted_count == 1:
                return Response(
                    response=json.dumps(
                        {"message": " Book information Deleted Successfully ! ", "id": f"{id}"}
                    ),
                    status=200,
                    mimetype='application/json'
                )
            else:
                return Response(
                    response=json.dumps(
                        {"message": " OOpsS!! Book not found anymore! ", "id": f"{id}"}
                    ),
                    status=404,
                    mimetype='application/json'
                )


        except Exception as ex:
            print("**********")
            print(ex)
            print("***********")
            return Response(
                response=json.dumps(
                    {"message": "Sorry ! :( can not delete "}
                ),
                status=500,
                mimetype='application/json'
            )

    else:
        return Response(
            response=json.dumps(
                {"message": "User is unauthorized to create book"
                 }
            ),
            status=403,
            mimetype='application/json'
        )


@app.route('/book/search', methods=['POST'])
@jwt_required
def search_book():
    try:
        dbResponse = searchBook(request.json)
        return Response(
            response=json.dumps(
                {
                    "User": f"{dbResponse}"
                }
            ),
            status=201,
            mimetype='application/json'
        )
    except:
        print("Failed")


########################################################

# User Service #########################################
def signIn(Object):
    try:
        email = Object['email']
        password = Object['password']
        dbResponse = db.users.find_one({'email': email})
        result = ""
        if dbResponse:
            if pwd_context.verify(password, dbResponse['password_hash']):
                try:
                    access_token = create_access_token(identity={
                        'firstName': dbResponse['firstName'],
                        'lastName': dbResponse['lastName'],
                        'email': dbResponse['email'],
                        'roles': dbResponse['roles']
                    })


                except Exception as ex:
                    print(ex)

                result = access_token
                return result
            else:
                result = "Error"
                return result
        else:
            result = "Error"
            return
    except Exception as ex:
        print('*********************')

        print(ex)
        print('********************')


def userSignUp(Object):
    try:
        firstName = Object['firstName']
        lastName = Object['lastName']
        email = Object['email']
        roles = Object['roles']
        password = Object['password']
        created = datetime.utcnow()
        dbResponse = db.users.find_one({'email': email})
        result = "exists"
        if dbResponse == None:
            userId = db.users.insert_one({
                'firstName': firstName,
                'lastName': lastName,
                'email': email,
                'roles': roles,
                'password_hash': pwd_context.encrypt(password),
                'createdAt': created,
            })
            result = userId
            return result
        else:
            return result
    except Exception as ex:
        print('*********************')

        print(ex)
        print('********************')


#############################################################

# Book Service ##############################################
# Create Book Service
def createBook(object):
    try:
        dbResponse = db.books.insert_one(object)
        return dbResponse

    except Exception as ex:
        print("88888")
        print(ex)


# See Book List Service
def seeBookList():
    try:

        booklist = list(db.books.find())
        for book in booklist:
            book["_id"] = str(book["_id"])
        return booklist


    except Exception as ex:
        print("88888")
        print(ex)


# Update Book Info Service
def updateBookInfo(id, obj):
    try:

        dbResponse = db.books.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"Bookname": obj.get('Bookname')}}

        )

        return dbResponse


    except Exception as ex:
        print(ex)


# Delete Book Info
def deleteBookInfo(id):
    try:
        dbResponse = db.books.delete_one({"_id": ObjectId(id)})
        return dbResponse
    except Exception as ex:
        print("####")
        print(ex)
        print("#######")


# Search Book
def searchBook(Object):
    try:

        regex_query = {"Bookname": {"$regex": Object.get('Bookname')}}
        dbResponse = list(db.books.find(regex_query))

        return dbResponse
    except:
        print("Failed")


#############################################################
# Validators ################################################
schema = Kanpai.Object({
    "firstName": Kanpai.String().max(20).trim().required("First Name required"),
    "lastName": Kanpai.String().max(20).trim().required("Last Name required"),
    "email": Kanpai.Email().required("email required"),
    "roles": Kanpai.String().max(5).trim().required("User Role Required"),
    "password": Kanpai.String().max(20).trim().required("pass required")
})
#############################################################

if __name__ == "__main__":
    app.run()
