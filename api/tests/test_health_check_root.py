import unittest
from unittest.mock import patch
from api.server import app


class TestHealthCheckRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True

    # Positive test
    def test_health_check(self):
        with app.test_client() as client:
            response = client.get('/health_check')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'status': 'OK'})
