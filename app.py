import json

import Service.BookService
import Service.UserService
import Validators.UserSignupValidation
from flask import Flask
from flask import Response, request
from bson.objectid import ObjectId
from datetime import datetime
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
import  Properties.DbConfiguration


from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)

app.config['SECRET_KEY']='Th1s1ss3cr3t'
jwt = JWTManager(app)



@app.route('/user/signUp', methods=['POST'])
def user_signup():
    validation_result = Validators.UserSignupValidation.schema.validate(request.json)
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
        dbResponse = Service.UserService.user_signup(userDetails)

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
##########################
@app.route('/user/signIn', methods=['POST'])
def user_signIn():
    try:
        userLogInDetails = request.get_json()
        dbResponse = signIn(userLogInDetails)
        if dbResponse.__eq__("Error"):
            return Response(
                response=json.dumps(
                    {"Error": "Faild"
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
#########################

@app.route('/admin/createBook', methods=['POST'])
@jwt_required
def create_book():
    try:
        bookDetails = request.get_json()
        dbResponse = Service.BookService.create_book(bookDetails)

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


@app.route('/user/BookList', methods=['GET'])
@jwt_required
def see_book_list():
    current_user = get_jwt_identity()
    print(current_user)
    try:
        booklist = Service.BookService.see_book_list()

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


@app.route('/admin/<id>', methods=['PATCH'])
@jwt_required
def update_book_info(id):
    try:
        dbResponse = Service.BookService.update_book_info(id, request.json)

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


@app.route('/admin/<id>', methods=['DELETE'])
@jwt_required
def delete_book_info(id):
    try:
        dbResponse = Service.BookService.delete_book_info(id)
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


@app.route('/book/search', methods=['POST'])
@jwt_required
def delete_book_info_one():
    try:
        dbResponse = Service.BookService.boi_khojo(request.json)
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
########################
def signIn(Object):
    try:
        email = Object['email']
        password = Object['password']
        dbResponse = Properties.DbConfiguration.db.users.find_one({'email':email})
        result = ""
        if dbResponse:
            if pwd_context.verify(password, dbResponse['password_hash']):
                try:
                    access_token = create_access_token(identity={
                        'firstName': dbResponse['firstName'],
                        'lastName': dbResponse['lastName'],
                        'email': dbResponse['email']
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

#######################


if __name__ == "__main__":
    app.run()
