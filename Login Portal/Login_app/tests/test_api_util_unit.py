import os
import unittest
from Login_app import api_util
from Login_app import db
from Login_app import app


def create_app():
    app.config['TESTING'] = True
    app.config['BASE_DIR'] = os.path.dirname(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests\\test_db.sqlite3'
    return app


app = create_app()
db.create_all()


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.fun = api_util

    def test_register(self):
        result = self.fun.check_credentials_post('user1', 'pass1', 'user@gmail.com')
        self.assertEqual(202, result)

    def test_register_again(self):
        result = self.fun.check_credentials_post('user1', 'pass1', 'user@gmail.com')
        self.assertEqual(208, result)

    def test_register_wrong_bad_entries_blank(self):
        result = self.fun.check_json_post({'username': "", 'password': 'pass1', 'email': 'user@gmail.com'})
        self.assertEqual(False, result)

    def test_register_wrong_bad_entries_integer(self):
        result = self.fun.check_json_post({'username': 123, 'password': 'pass1', 'email': 'user@gmail.com'})
        self.assertEqual(False, result)

    def test_login(self):
        result = self.fun.check_credentials_put('user1', 'pass1')
        self.assertEqual(202, result)

    def test_login_wrong_password(self):
        result = self.fun.check_credentials_put('user1', 'wrong_password')
        self.assertEqual("401_password_not_matching", result)

    def test_login_user_not_added(self):
        result = self.fun.check_credentials_put('user2', 'pass2')
        self.assertEqual("401_user_not_found", result)

    def test_login_wrong_bad_entries_blank(self):
        result = self.fun.check_json_put({'username': '', 'password': ''})
        self.assertEqual(False, result)

    def test_login_wrong_bad_entries_integer(self):
        result = self.fun.check_json_put({'username': 123, 'password': 'user1'})
        self.assertEqual(False, result)


if __name__ == '__main__':
    unittest.main()
