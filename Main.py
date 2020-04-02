import json
import Service.BookService
import Service.UserService
from flask import Flask, jsonify
from flask import Response, request
import Validators.UserSignupValidation



app = Flask(__name__)


@app.route('/user/signUp', methods=['POST'])
def user_signup():
    validation_result= Validators.UserSignupValidation.schema.validate(request.json)
    if validation_result.get('success',False) is False:
        return jsonify({
            "Status": "Error",
            "Error": validation_result.get("error")

        })
    try:
        userDetails = request.get_json()
        dbResponse = Service.UserService.user_signup(userDetails)


        return Response(
            response=json.dumps(
                {"user": "User created Successfully",
                 "userId": f"{dbResponse.inserted_id}"
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



@app.route('/admin/createBook', methods= ['POST'])
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
def see_book_list():
     try:
         booklist= Service.BookService.see_book_list()

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
def update_book_info(id):

     try:
         dbResponse = Service.BookService.update_book_info(id,request.json)


         if dbResponse.modified_count ==1:
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
             status=500,
             mimetype='application/json'
         )
@app.route('/admin/<id>', methods=['DELETE'])
def delete_book_info(id):
    try:
        dbResponse= Service.BookService.delete_book_info(id)
        if dbResponse.deleted_count == 1:
            return Response(
            response=json.dumps(
                {"message": " Book information Deleted Successfully ! ","id": f"{id}"}
            ),
            status=200,
            mimetype='application/json'
        )
        else:
            return Response(
                response=json.dumps(
                    {"message": " OOpsS!! Book not found anymore! ", "id": f"{id}"}
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
                {"message": "Sorry ! :( can not delete "}
            ),
            status=500,
            mimetype='application/json'
        )












if __name__ == "__main__":
    app.run()
