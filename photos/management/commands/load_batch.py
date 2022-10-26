from django.core.management.base import BaseCommand, CommandError
from requests import get, JSONDecodeError

from photos.models import Photo
from photos.utils import parse_url, validate_url


class Command(BaseCommand):
    help = 'Loads batch of photos'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str)

    def handle(self, *args, **options):
        json_url = options['json_url']

        try:
            validated_url = validate_url(json_url)
        except ValueError as e:
            raise CommandError(f'Invalid URL: {json_url}') from e

        try:
            json_content = get(validated_url).json()
        except JSONDecodeError as e:
            raise CommandError(f'Invalid JSON: {validated_url}') from e

        for photo_data in json_content:
            try:
                _id = photo_data['id']
                title = photo_data['title']
                album_id = photo_data['albumId']
                photo_url = photo_data['url']
            except KeyError as e:
                raise CommandError(f'Invalid JSON keys: {photo_data}') from e

            if Photo.objects.filter(pk=_id).exists():
                self.stdout.write(self.style.WARNING(f'The photo loaded from {photo_url} already exists'))
                continue

            photo = parse_url(photo_url)
            photo.id = _id
            photo.title = title
            photo.album_id = album_id
            photo.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded photos from {json_url}'))
