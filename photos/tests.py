from io import StringIO

from django.core.management import call_command, CommandError
from django.test import TestCase

from photos import utils


# TODO: check tests!!! They broke
class UtilsTest(TestCase):
    def setUp(self):
        pass

    def test_parse_url_path_valid(self):
        width, height, color, ext = utils.parse_url_path('https://via.placeholder.com/600/92c952')
        self.assertEqual(width, 600)
        self.assertEqual(height, 600)
        self.assertEqual(color, '#92c952')
        self.assertEqual(ext, '')

    def test_parse_url_path_valid_with_ext(self):
        width, height, color, ext = utils.parse_url_path('https://via.placeholder.com/600/92c952.png')
        self.assertEqual(width, 600)
        self.assertEqual(height, 600)
        self.assertEqual(color, '#92c952')
        self.assertEqual(ext, '.png')

    def test_parse_url_path_invalid(self):
        with self.assertRaises(IndexError):
            utils.parse_url_path('https://www.example.com/')

    def test_validate_url_invalid(self):
        invalid_urls = [
            'www.example.com',  # no protocol
            'https://www.example.com',  # no path
            'https://www.example.com/'  # no file
        ]
        for url in invalid_urls:
            with self.assertRaises(ValueError):
                utils.validate_photo_url(url)

    def test_validate_url_valid(self):
        valid_urls = [
            'https://via.placeholder.com/600/92c952',
            'https://via.placeholder.com/600/21d35'
            'https://via.placeholder.com/600/21d35.png'
        ]
        for url in valid_urls:
            validated_url = utils.validate_photo_url(url)
            self.assertEqual(validated_url, url)

    def test_parse_url_valid(self):
        photo = utils.photo_from_url('https://via.placeholder.com/600/92c952.png')
        self.assertEqual(photo.width, 600)
        self.assertEqual(photo.height, 600)
        self.assertEqual(photo.color, '#92c952')

    def test_parse_url_invalid(self):
        with self.assertRaises(IndexError):
            utils.photo_from_url('https://via.placeholder.com/600')

    def test_parse_url_valid_ext_invalid(self):
        with self.assertRaisesMessage(ValueError, 'Invalid file format: text/html; charset=UTF-8 or extension: .fake'):
            utils.photo_from_url('https://via.placeholder.com/600/92c952.fake')


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
