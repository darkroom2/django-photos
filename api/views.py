from io import BytesIO
from urllib.parse import urlparse

from django.core.files.uploadedfile import UploadedFile
from requests import get
from rest_framework import generics

from api.serializers import PhotoSerializer
from photos.models import Photo


class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def perform_create(self, serializer):
        # TODO validation if url is valid and contains information on width, height and color. If not try to get it
        #  from the image
        url = serializer.validated_data['remote_url']
        url_resolved = urlparse(url)
        parts = url_resolved.path.split('/')[1:]
        width = height = parts[0]
        color = f'#{parts[1]}'
        ext = 'png'
        file_name = f'{width}x{height}_{color[1:]}.{ext}'
        image_data = get(f'{url}.{ext}').content
        serializer.validated_data['image'] = UploadedFile(BytesIO(image_data), name=file_name)
        serializer.save(width=width, height=height, color=color)
