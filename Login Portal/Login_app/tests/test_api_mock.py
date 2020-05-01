import json
import unittest
from unittest.mock import patch
from Login_app import app


class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('Login_app.api_util.check_credentials_post')
    @patch('Login_app.api_util.check_json_post')
    def test_register_user_added(self, mock_json, mock_post):
        mock_json.return_value = True
        mock_post.return_value = 202
        result = self.app.post('/register/',
                               data=json.dumps({'username': 'user1', 'password': 'pass1', 'email': 'user@gmail.com'}),
                               content_type='application/json')
        data_received = result.get_json()
        self.assertEqual(result.status_code, 202)
        self.assertEqual(data_received["status"], "Added New User")

    @patch('Login_app.api_util.check_credentials_post')
    @patch('Login_app.api_util.check_json_post')
    def test_register_bad_entry(self, mock_json, mock_post):
        mock_json.return_value = False
        mock_post.return_value = 202
        result = self.app.post('/register/',
                               data=json.dumps({'username': 'user1', 'password': 'pass1', 'email': 'user@gmail.com'}),
                               content_type='application/json')
        self.assertEqual(result.status_code, 400)

    @patch('Login_app.api_util.check_credentials_post')
    @patch('Login_app.api_util.check_json_post')
    def test_register_already_exist(self, mock_json, mock_post):
        mock_json.return_value = True
        mock_post.return_value = 208
        result = self.app.post('/register/',
                               data=json.dumps({'username': 'user1', 'password': 'pass1', 'email': 'user@gmail.com'}),
                               content_type='application/json')
        self.assertEqual(result.status_code, 208)

    @patch('Login_app.api_util.check_credentials_post')
    @patch('Login_app.api_util.check_json_post')
    def test_register_database_error(self, mock_json, mock_post):
        mock_json.return_value = True
        mock_post.return_value = 503
        result = self.app.post('/register/',
                               data=json.dumps({'username': 'user1', 'password': 'pass1', 'email': 'user@gmail.com'}),
                               content_type='application/json')
        self.assertEqual(result.status_code, 503)

    @patch('Login_app.api_util.check_credentials_put')
    @patch('Login_app.api_util.check_json_put')
    def test_login(self, mock_json, mock_put):
        mock_json.return_value = True
        mock_put.return_value = 202
        result = self.app.put('/login/',
                              data=json.dumps({'username': 'user1', 'password': 'pass1'}),
                              content_type='application/json')
        self.assertEqual(result.status_code, 202)

    @patch('Login_app.api_util.check_credentials_put')
    @patch('Login_app.api_util.check_json_put')
    def test_login_user_not_exist(self, mock_json, mock_put):
        mock_json.return_value = True
        mock_put.return_value = "401_user_not_found"
        result = self.app.put('/login/',
                              data=json.dumps({'username': 'wrong_username', 'password': 'pass1'}),
                              content_type='application/json')
        self.assertEqual(result.status_code, 401)

    @patch('Login_app.api_util.check_credentials_put')
    @patch('Login_app.api_util.check_json_put')
    def test_login_password_wrong(self, mock_json, mock_put):
        mock_json.return_value = True
        mock_put.return_value = "401_password_not_matching"
        result = self.app.put('/login/',
                              data=json.dumps({'username': 'user1', 'password': 'wrong_password'}),
                              content_type='application/json')
        self.assertEqual(result.status_code, 401)

    @patch('Login_app.api_util.check_credentials_put')
    @patch('Login_app.api_util.check_json_put')
    def test_login_bad_entry(self, mock_json, mock_put):
        mock_json.return_value = False
        mock_put.return_value = 202
        result = self.app.put('/login/',
                              data=json.dumps({'username': 'user1', 'password': 'pass1'}),
                              content_type='application/json')
        self.assertEqual(result.status_code, 400)

    @patch('Login_app.api_util.check_credentials_put')
    @patch('Login_app.api_util.check_json_put')
    def test_login_database_error(self, mock_json, mock_put):
        mock_json.return_value = True
        mock_put.return_value = 503
        result = self.app.put('/login/',
                              data=json.dumps({'username': 'user1', 'password': 'pass1'}),
                              content_type='application/json')
        self.assertEqual(result.status_code, 503)


if __name__ == '__main__':
    unittest.main()
