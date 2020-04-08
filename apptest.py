import unittest

from app import app
import json

class TestMyBookLibraryApp(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.data = {"Bookname": '', "Authorname": ''}
        self.da={"data is created"}


    # def test_create_book(self):
    #     response= self.client.post(path='/admin/createBook', data= json.dumps(self.data), content_type='application/json')
    #     self.assertEqual(response.status_code,201)
    #     self.assertEqual(response.json['message':"Book created Successfully",201])
    #     self.assertEqual(response.json["msg"],' book created')

    def  test_see_book_list(self):
        response = self.client.get(path='/user/BookList', content_type= 'application/json')
        self.assertEqual(response.status_code,200)
    #
    #
    def test_update_book_info(self):
        p = self.client.patch(path= '/admin/<id>', data= json.dumps(self.data), content_type= 'application/json')
        book_id = bytes(p.json[id])
        path= '/admin/{}'.format(book_id)
        response= self.client.patch(path,data=json.dumps(self.da),content_type= 'application/json')
        self.assertEqual(response.status_code,200)
    #
    # def test_delete_book_info(self):
    #     post = self.client.post(path='/admin/<id>', data=json.dumps(self.data), content_type='application/json')
    #     book_id = int(post.json['_id'])
    #     path = '/admin/{}'.format(book_id)
    #     response = self.client.patch(path,  content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #


    def tearDown(self):
     pass

if __name__ == '__main__':
    unittest.main()
