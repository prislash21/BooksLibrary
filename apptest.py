import json
import unittest

import pymongo
from app import app, db


class UserSignUpTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db

    # User signUp with all required data
    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash291@gmail1.com",
            "roles": "USER",
            "password": "abc123@"
        })

        # When
        response = self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=payload)
        # Then
        self.assertEqual(201, response.status_code)

    # User signUp with existing email
    def test_existing_email_signup(self):
        # Given
        payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash299@gmail1.com",
            "roles": "USER",
            "password": "abc123@"
        })

        # When
        response = self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=payload)
        response1 = self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(409, response1.status_code)

    # Successfull login with valid credentials
    def test_successful_login(self):
        # SignUp Payload
        signUp_payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash299@gmail1.com",
            "roles": "USER",
            "password": "abc123@"
        })

        self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=signUp_payload)

        # Given
        email = "prislash299@gmail1.com"
        password = "abc123@"
        payload = json.dumps({
            "email": email,
            "password": password
        })
        response = self.app.post('', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.post('/user/signIn', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['user']))
        self.assertEqual(201, response.status_code)

    # Unsuccessfull login with invalid credentials
    def test_unsuccessful_login_wrongpassword(self):
        # SignUp Payload
        signUp_payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash299@gmail1.com",
            "roles": "USER",
            "password": "abc123@"
        })

        self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=signUp_payload)

        # Given
        email = "prislash299@gmail1.com"
        password = "abc123"
        payload = json.dumps({
            "email": email,
            "password": password
        })
        response = self.app.post('', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.post('/user/signIn', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(400, response.status_code)

    # Create book by ADMIN
    def test_create_book_by_ADMIN(self):
        # SignUp Payload
        signUp_payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash290@gmail1.com",
            "roles": "ADMIN",
            "password": "abc123@"
        })

        self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=signUp_payload)

        # SignIn Portion
        email = "prislash290@gmail1.com"
        password = "abc123@"
        userSignIn_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('', headers={"Content-Type": "application/json"}, data=userSignIn_payload)
        response = self.app.post('/user/signIn', headers={"Content-Type": "application/json"}, data=userSignIn_payload)
        login_token = response.json['user']

        book_payload = {
            "Bookname": "Maamani",
            "Authorname": "Maxim Gorci"
        }
        # When
        response = self.app.post('/book/createBook',
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(book_payload))

        # Then
        self.assertEqual(str, type(response.json['bookId']))
        self.assertEqual(201, response.status_code)

    # Create book by USER
    def test_create_book_by_USER(self):
        # SignUp Payload
        signUp_payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash290@gmail1.com",
            "roles": "USER",
            "password": "abc123@"
        })

        self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=signUp_payload)

        # SignIn Portion
        email = "prislash290@gmail1.com"
        password = "abc123@"
        userSignIn_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('', headers={"Content-Type": "application/json"}, data=userSignIn_payload)
        response = self.app.post('/user/signIn', headers={"Content-Type": "application/json"},
                                 data=userSignIn_payload)
        login_token = response.json['user']

        book_payload = {
            "Bookname": "Maamani",
            "Authorname": "Maxim Gorci"
        }
        # When
        response = self.app.post('/book/createBook',
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(book_payload))

        # Then
        self.assertEqual(403, response.status_code)

    # Getting book list after login
    def test_get_books(self):
        # SignUp Payload
        signUp_payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash290@gmail1.com",
            "roles": "USER",
            "password": "abc123@"
        })

        self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=signUp_payload)

        # SignIn Portion
        email = "prislash290@gmail1.com"
        password = "abc123@"
        userSignIn_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('', headers={"Content-Type": "application/json"}, data=userSignIn_payload)
        response = self.app.post('/user/signIn', headers={"Content-Type": "application/json"},
                                 data=userSignIn_payload)
        login_token = response.json['user']
        response = self.app.get('/book/bookList', headers={"Content-Type": "application/json",
                                                           "Authorization": f"Bearer {login_token}"})
        self.assertEqual(200, response.status_code)

    def test_search_book(self):
        # SignUp Payload
        signUp_payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash290@gmail1.com",
            "roles": "USER",
            "password": "abc123@"
        })

        self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=signUp_payload)

        # SignIn Portion
        email = "prislash290@gmail1.com"
        password = "abc123@"
        userSignIn_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('', headers={"Content-Type": "application/json"}, data=userSignIn_payload)
        response = self.app.post('/user/signIn', headers={"Content-Type": "application/json"},
                                 data=userSignIn_payload)
        login_token = response.json['user']
        search_payload = {
            "Bookname": "Maamani"
        }
        # When
        response = self.app.post('/book/search',
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(search_payload))

        # Then
        self.assertEqual(201, response.status_code)

    def test_update_book(self):
        # SignUp Payload
        signUp_payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash290@gmail1.com",
            "roles": "ADMIN",
            "password": "abc123@"
        })

        self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=signUp_payload)

        # SignIn Portion
        email = "prislash290@gmail1.com"
        password = "abc123@"
        userSignIn_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('', headers={"Content-Type": "application/json"}, data=userSignIn_payload)
        response = self.app.post('/user/signIn', headers={"Content-Type": "application/json"},
                                 data=userSignIn_payload)
        login_token = response.json['user']
        book_payload = {
            "Bookname": "Maamani",
            "Authorname": "Maxim Gorci"
        }
        # When
        response1 = self.app.post('/book/createBook',
                                  headers={"Content-Type": "application/json",
                                           "Authorization": f"Bearer {login_token}"},
                                  data=json.dumps(book_payload))
        update_payload = {
            "Bookname": "Mama"
        }
        bookId = response1.json["bookId"]
        response2 = self.app.patch(f"/book/updateBook/{bookId}",
                                   headers={"Content-Type": "application/json",
                                            "Authorization": f"Bearer {login_token}"},
                                   data=json.dumps(book_payload))
        self.assertEqual(200, response2.status_code)

    def test_delete_book(self):
        # SignUp Payload
        signUp_payload = json.dumps({
            "firstName": "Priota",
            "lastName": "Roy",
            "email": "prislash290@gmail1.com",
            "roles": "ADMIN",
            "password": "abc123@"
        })

        self.app.post('/user/signUp', headers={"Content-Type": "application/json"}, data=signUp_payload)

        # SignIn Portion
        email = "prislash290@gmail1.com"
        password = "abc123@"
        userSignIn_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('', headers={"Content-Type": "application/json"}, data=userSignIn_payload)
        response = self.app.post('/user/signIn', headers={"Content-Type": "application/json"},
                                 data=userSignIn_payload)
        login_token = response.json['user']
        book_payload = {
            "Bookname": "Maamani",
            "Authorname": "Maxim Gorci"
        }
        # When
        response1 = self.app.post('/book/createBook',
                                  headers={"Content-Type": "application/json",
                                           "Authorization": f"Bearer {login_token}"},
                                  data=json.dumps(book_payload))
        update_payload = {
            "Bookname": "Mama"
        }
        bookId = response1.json["bookId"]
        response2 = self.app.delete(f"/book/deleteBook/{bookId}",
                                    headers={"Content-Type": "application/json",
                                             "Authorization": f"Bearer {login_token}"},
                                    data=json.dumps(book_payload))
        self.assertEqual(200, response2.status_code)

    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)


if __name__ == "__main__":
    unittest.main()
