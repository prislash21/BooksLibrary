import Properties.DbConfiguration
from datetime import datetime
from bson.objectid import ObjectId
from passlib.apps import custom_app_context as pwd_context



def user_signup(Object):
    try:
        firstName = Object['firstName']
        lastName = Object['lastName']
        email = Object['email']
        password = Object['password']
        created = datetime.utcnow()

        userId = Properties.DbConfiguration.db.users.insert_one({
            'firstName': firstName,
            'lastName': lastName,
            'email': email,
            'password_hash': pwd_context.encrypt(password),
            'createdAt': created,
        })
        result = {'userId': userId}
        return result;

    except Exception as ex:
        print('*********************')

        print(ex)
        print('********************')