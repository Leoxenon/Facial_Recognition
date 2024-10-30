import unittest
from app import app
import json

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        
    def test_login_missing_fields(self):
        response = self.app.post('/api/auth/login',
            json={
                'username': 'test',
                'password': 'test'
            }
        )
        self.assertEqual(response.status_code, 400)
