from django.test import TestCase

from photos.utils import parse_url, validate_url


# Create your tests here.
class UtilsTestCase(TestCase):
    def setUp(self):
        pass

    def test_validate_url_invalid(self):
        invalid_urls = [
            'www.example.com',  # no protocol
            'https://www.example.com',  # no path
            'https://www.example.com/'  # no file
        ]
        for url in invalid_urls:
            with self.assertRaises(ValueError):
                validate_url(url)

    def test_validate_url_valid(self):
        valid_urls = [
            'https://via.placeholder.com/600/92c952',
            'https://via.placeholder.com/600/21d35'
        ]
        for url in valid_urls:
            validated_url = validate_url(url)
            self.assertEqual(validated_url, url)

    def test_parse_url_valid(self):  # TODO: add mocking file download
        valid_data = [
            ('https://via.placeholder.com/600/92c952', 600, 600, '#92c952'),
            ('https://via.placeholder.com/600/21d35', 600, 600, '#21d350')
        ]
        for url, width, height, color in valid_data:
            photo = parse_url(url)
            self.assertEqual(photo.width, width)
            self.assertEqual(photo.height, height)
            self.assertEqual(photo.color, color)

    def test_parse_url_valid_custom(self):
        valid_url = 'https://via.placeholder.com/600'
        photo = parse_url(valid_url)
        self.assertEqual(photo.width, 600)
        self.assertEqual(photo.height, 600)
        self.assertEqual(photo.color, '#cccccc')
