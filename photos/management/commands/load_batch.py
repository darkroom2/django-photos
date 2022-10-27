from multiprocessing.dummy import Pool

from django.core.management.base import BaseCommand

from photos import utils
from photos.models import Photo


class Command(BaseCommand):
    help = 'Loads batch of photos'

    def add_arguments(self, parser):
        parser.add_argument('json', type=str, help='URL or JSON file')

    def handle(self, *args, **options):
        json_url = options['json']

        json_content = utils.get_json(json_url)  # list of dicts

        files_count = len(json_content)

        # TODO: try using serializers????
        with Pool() as pool:  # threading in I/O bound tasks might increase performance
            results = pool.map(utils.photo_from_json, json_content)

        photos_to_save = list(filter(lambda x: x, results))

        if photos_to_save:
            Photo.objects.bulk_create(photos_to_save)

        skipped_files_count = files_count - len(photos_to_save)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded photos: {files_count - skipped_files_count}, skipped: {skipped_files_count}'
            )
        )
