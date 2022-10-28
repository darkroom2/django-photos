from io import BytesIO
from pathlib import Path

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management.base import BaseCommand

from api import serializers


class Command(BaseCommand):
    help = 'Loads batch of photos'

    def add_arguments(self, parser):
        parser.add_argument('json', type=str, help='URL or JSON file path')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--url', action='store_true', help='Provided JSON is URL')
        group.add_argument('--file', action='store_true', help='Provided JSON is file')

    def handle(self, *args, **options):
        data = {}

        if options.get('url'):
            data['json_url'] = options['json']

        elif options.get('file'):
            file_path = Path(options['json'])
            file_data = BytesIO(file_path.read_bytes())
            data['json_file'] = InMemoryUploadedFile(file=file_data, field_name='json_file', name=file_path.name,
                                                     content_type='*/*', size=file_data.getbuffer().nbytes,
                                                     charset='utf-8')

        serializer = serializers.PhotosUploadSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        photos = serializer.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded photos: {len(photos.validated_data)}'))
