from rest_framework import generics

from api.serializers import PhotoSerializer, PhotosUploadSerializer
from photos.models import Photo


class PhotoListCreate(generics.ListCreateAPIView):
    """
    GET: List all photos
    POST: Create a new photo
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a photo
    PUT: Update a photo
    PATCH: Partial update a photo
    DELETE: Delete a photo
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotosUploadCreate(generics.CreateAPIView):
    """
    POST: Upload photos from external api
    """
    serializer_class = PhotosUploadSerializer
