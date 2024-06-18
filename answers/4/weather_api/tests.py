import unittest
from app import app, db
from models import WeatherData, WeatherStats

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_weather(self):
        response = self.app.get('/api/weather')
        self.assertEqual(response.status_code, 200)

    def test_get_weather_stats(self):
        response = self.app.get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
