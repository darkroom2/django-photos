from unittest import mock

from rest_framework.test import APITestCase

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


class TestPhotosListView(APITestCase):
    def test_get_photos(self):
        _ = create_photo()
        response = self.client.get('/api/photos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    @mock.patch('photos.utils.photo_from_url')
    def test_post_photo(self, mock_photo_from_url):
        data = {
            'title': 'Photo 1',
            'album_id': 1,
            'remote_url': 'https://via.placeholder.com/600/92c952',
        }
        response = self.client.post('/api/photos/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Photo.objects.count(), 1)
