import shutil

from django.conf import settings
from rest_framework.test import APITestCase, override_settings

from photos.models import Photo


def create_photo():
    return Photo.objects.create(
        title='Photo 1',
        album_id=1,
        remote_url='https://via.placeholder.com/600/92c952',
        width=600,
        height=600,
        color='#92c952'
    )


@override_settings(MEDIA_ROOT=settings.BASE_DIR / 'tmp')
class TestPhotosListView(APITestCase):
    @classmethod
    def tearDownClass(cls):
        if settings.MEDIA_ROOT.exists():
            shutil.rmtree(settings.MEDIA_ROOT)

    def test_get_photos(self):
        _ = create_photo()
        response = self.client.get('/api/photos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), Photo.objects.count())

    def test_post_photo(self):
        data = {
            'title': 'Photo 1',
            'album_id': 1,
            'remote_url': 'https://via.placeholder.com/600/92c952'
        }
        response = self.client.post('/api/photos/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Photo.objects.count(), 1)
