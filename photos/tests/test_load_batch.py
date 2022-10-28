import shutil
from io import StringIO
from unittest import skip

from django.conf import settings
from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings
from rest_framework.exceptions import ValidationError


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'tmp')
class TestLoadBatchCommand(TestCase):
    @classmethod
    def tearDownClass(cls):
        if settings.MEDIA_ROOT.exists():
            shutil.rmtree(settings.MEDIA_ROOT)

    def test_missing_args(self):
        with self.assertRaises(CommandError):
            call_command('load_batch')

    def test_with_url_missing_positional_arg(self):
        with self.assertRaises(CommandError):
            call_command('load_batch', '--url')

    def test_with_file_missing_positional_arg(self):
        with self.assertRaises(CommandError):
            call_command('load_batch', '--file')

    def test_missing_file_url_with_positional_arg(self):
        with self.assertRaises(CommandError):
            call_command('load_batch', 'url')

    def test_missing_file_url_with_multiple_positional_args(self):
        with self.assertRaises(CommandError):
            call_command('load_batch', 'url', 'url2')

    def test_file_with_multiple_positional_args(self):
        with self.assertRaises(CommandError):
            call_command('load_batch', 'url', 'url2', '--file')

    def test_mutual_excluding_args(self):
        with self.assertRaises(CommandError):
            call_command('load_batch', 'url', '--file', '--url')

    def test_url_with_invalid_positional_arg(self):
        with self.assertRaises(ValidationError):
            call_command('load_batch', 'url', '--url')

    def test_file_with_invalid_positional_arg(self):
        with self.assertRaises(FileNotFoundError):
            call_command('load_batch', 'url', '--file')

    def test_file_valid(self):
        out = StringIO()
        call_command('load_batch', 'test_data/photos_small.json', '--file', stdout=out)
        message = 'Successfully loaded photos: 30'
        self.assertIn(message, out.getvalue())

    def test_file_valid_wrong_format(self):
        with self.assertRaises(ValidationError):
            call_command('load_batch', 'test_data/photos_invalid.json', '--file')

    def test_file_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            call_command('load_batch', 'fake/path/to/file.json', '--file')

    def test_url_with_file_arg(self):
        with self.assertRaises(FileNotFoundError):
            call_command('load_batch', 'https://example.com/', '--file')

    def test_file_with_url_arg(self):
        with self.assertRaises(ValidationError):
            call_command('load_batch', 'fake/path/to/file.json', '--url')

    def test_url_invalid(self):
        with self.assertRaises(ValidationError):
            call_command('load_batch', 'https://jsonplaceholder.typicode.com/', '--url')

    @skip("long running test, takes ~8min")
    def test_url_valid(self):
        out = StringIO()
        call_command('load_batch', 'https://jsonplaceholder.typicode.com/photos', '--url', stdout=out)
        message = 'Successfully loaded photos: 5000, skipped: 0'
        self.assertIn(message, out.getvalue())

    def test_url_valid_wrong_format(self):
        with self.assertRaises(ValidationError):
            call_command('load_batch', 'https://jsonplaceholder.typicode.com/posts', '--url')
