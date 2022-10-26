from io import StringIO

from django.core.management import call_command, CommandError
from django.test import TestCase

from photos.utils import parse_url, validate_url


class UtilsTest(TestCase):
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
        self.assertEqual(photo.width, 0)
        self.assertEqual(photo.height, 0)
        self.assertEqual(photo.color, '#ffffff')


class LoadBatchCommandTest(TestCase):
    def test_missing_arg(self):
        with self.assertRaises(CommandError):
            call_command('load_batch')

    def test_multiple_positional_args(self):
        with self.assertRaises(CommandError):
            call_command('load_batch', 'url', 'url2')

    def test_invalid_positional_arg(self):
        with self.assertRaises(FileNotFoundError):
            call_command('load_batch', 'url')

    def test_json_file_valid(self):  # TODO: add mocking file write
        out = StringIO()
        call_command('load_batch', 'test_data/photos_small.json', stdout=out)
        message = 'Successfully loaded photos: 30, skipped: 0'
        self.assertIn(message, out.getvalue())

    def test_json_file_invalid(self):  # TODO: add mocking file write
        out = StringIO()
        call_command('load_batch', 'test_data/photos_invalid.json', stdout=out)
        message = 'Successfully loaded photos: 0, skipped: 4'
        self.assertIn(message, out.getvalue())

    def test_json_file_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            call_command('load_batch', 'fake/path/to/file.json')

    # def test_json_url_valid(self):  # TODO: add mocking file download, add mocking file write
    #     out = StringIO()
    #     call_command('load_batch', 'https://jsonplaceholder.typicode.com/photos', stdout=out)
    #     success_message = 'Successfully loaded photos: 5000, skipped: 0'
    #     self.assertIn(success_message, out.getvalue())

    def test_json_url_invalid(self):
        with self.assertRaises(FileNotFoundError):
            call_command('load_batch', 'https://jsonplaceholder.typicode.com/')
