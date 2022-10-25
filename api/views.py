from rest_framework import generics

from api.serializers import PhotoSerializer
from photos.models import Photo


class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
