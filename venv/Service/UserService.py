import Properties.DbConfiguration



def user_signup(object):
    try:
        dbResponse = Properties.DbConfiguration.db.users.insert_one(object)
        return dbResponse

    except Exception as ex:
        print("*******")
        print(ex)