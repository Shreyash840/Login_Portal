import json
import os
import unittest
from Login_app import app
from Login_app import db


def create_app():
    app.config['TESTING'] = True
    app.config['BASE_DIR'] = os.path.dirname(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests\\test_db.sqlite3'

    return app


app = create_app()
db.create_all()


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_register(self):
        result = self.app.post('/register/',
                               data=json.dumps({'username': 'user1', 'password': 'pass1', 'email': 'user@gmail.com'}),
                               content_type='application/json')
        json_received = result.get_json()
        self.assertEqual(result.status_code, 202)
        self.assertEqual('Added New User', json_received['status'])

    def test_register_again(self):
        result = self.app.post('/register/',
                               data=json.dumps({'username': 'user1', 'password': 'pass1', 'email': 'user@gmail.com'}),
                               content_type='application/json')
        json_received = result.get_json()
        self.assertEqual(result.status_code, 208)
        self.assertEqual('Already Exists', json_received['status'])

    def test_register_with_bad_entries_blank(self):
        result = self.app.post('/register/',
                               data=json.dumps({'username': "", 'password': 'pass1', 'email': 'user@gmail.com'}),
                               content_type='application/json')
        self.assertEqual(result.status_code, 400)
        json_received = result.get_json()
        self.assertEqual("Bad Entries", json_received['status'])

    def test_register_with_bad_entries_integer(self):
        result = self.app.post('/register/',
                               data=json.dumps({'username': 123, 'password': 'pass1', 'email': 'user@gmail.com'}),
                               content_type='application/json')
        self.assertEqual(result.status_code, 400)
        json_received = result.get_json()
        self.assertEqual("Bad Entries", json_received['status'])

    def test_login(self):
        result = self.app.put('/login/',
                              data=json.dumps({'username': 'user1', 'password': 'pass1'}),
                              content_type='application/json')

        self.assertEqual(result.status_code, 202)
        json_received = result.get_json()
        self.assertEqual("Login successful", json_received['status'])

    def test_login_wrong_password(self):
        result = self.app.put('/login/',
                              data=json.dumps({'username': 'user1', 'password': 'wrong_password'}),
                              content_type='application/json')

        self.assertEqual(result.status_code, 401)
        json_received = result.get_json()
        self.assertEqual("Password does not match", json_received['status'])

    def test_login_wrong_bad_entries_blank(self):
        result = self.app.put('/login/',
                              data=json.dumps({'username': '', 'password': ''}),
                              content_type='application/json')

        self.assertEqual(result.status_code, 400)
        json_received = result.get_json()
        self.assertEqual("Bad Entries", json_received['status'])

    def test_login_wrong_bad_entries_integer(self):
        result = self.app.put('/login/',
                              data=json.dumps({'username': 123, 'password': 'wrong_password'}),
                              content_type='application/json')

        self.assertEqual(result.status_code, 400)
        json_received = result.get_json()
        self.assertEqual("Bad Entries", json_received['status'])

    def test_login_user_not_added(self):
        result = self.app.put('/login/',
                              data=json.dumps({'username': 'user2', 'password': 'pass2'}),
                              content_type='application/json')

        self.assertEqual(result.status_code, 401)
        json_received = result.get_json()
        self.assertEqual("User does not exist", json_received['status'])
