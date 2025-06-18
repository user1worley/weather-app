import unittest
from weather_app import get_weather_description, get_coordinates, get_weather_data

class TestWeatherApp(unittest.TestCase):
    def test_weather_description(self):
        """Test weather code to description conversion"""
        self.assertEqual(get_weather_description(0), "Clear sky")
        self.assertEqual(get_weather_description(95), "Thunderstorm")
        self.assertEqual(get_weather_description(999), "Unknown")

    def test_get_coordinates(self):
        """Test coordinate retrieval for a known city"""
        lat, lon, success = get_coordinates("London")
        self.assertTrue(success)
        self.assertIsNotNone(lat)
        self.assertIsNotNone(lon)
        self.assertTrue(51.0 <= lat <= 52.0)  # London's approximate latitude
        self.assertTrue(-0.5 <= lon <= 0.5)   # London's approximate longitude

    def test_get_coordinates_invalid_city(self):
        """Test coordinate retrieval for an invalid city"""
        lat, lon, success = get_coordinates("ThisCityDoesNotExist12345")
        self.assertFalse(success)
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    def test_get_weather_data(self):
        """Test weather data retrieval"""
        # Test with London coordinates
        weather_data, success = get_weather_data(51.5074, -0.1278)
        self.assertTrue(success)
        self.assertIsNotNone(weather_data)
        self.assertIn("current_weather", weather_data)
        self.assertIn("hourly", weather_data)

if __name__ == '__main__':
    unittest.main()