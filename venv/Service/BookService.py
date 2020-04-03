import  Properties.DbConfiguration
from bson.objectid import ObjectId

###########
def create_book(object):

    try:
        dbResponse = Properties.DbConfiguration.db.books.insert_one(object)
        return dbResponse

    except Exception as ex:
        print("88888")
        print(ex)

########

def see_book_list():
    try:

        booklist = list(Properties.DbConfiguration.db.books.find())
        for book in booklist:
            book["_id"] = str(book["_id"])
        return booklist


    except Exception as ex:
        print("88888")
        print(ex)

#####
def update_book_info(id,obj):

    try:

        dbResponse = Properties.DbConfiguration.db.books.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"Bookname": obj.get('Bookname')}}

        )

        return dbResponse


    except Exception as ex:
        print("88888")
        print(ex)
##############
def delete_book_info(id):
    try:
        dbResponse = Properties.DbConfiguration.db.books.delete_one({"_id": ObjectId(id)})
        return dbResponse
    except Exception as ex:
        print("####")
        print(ex)
        print("#######")

####################

def boi_khojo(Object):
    try:

        regex_query = {"Bookname": {"$regex": Object.get('Bookname')}}
        dbResponse = list(Properties.DbConfiguration.db.books.find(regex_query))

        return dbResponse
    except:
        print("Failed")

