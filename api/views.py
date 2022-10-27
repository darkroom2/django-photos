from rest_framework import generics

from api.serializers import PhotoSerializer, PhotosUploadSerializer
from photos.models import Photo


class PhotoListCreate(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotosUploadCreate(generics.CreateAPIView):
    serializer_class = PhotosUploadSerializer
