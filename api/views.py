from rest_framework import generics

from api.serializers import PhotoSerializer, PhotosUploadSerializer
from photos import utils
from photos.models import Photo


class PhotoListCreate(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    # TODO: make validations inside serializer, but also here for the url to the image, before serializer and its
    #  validator is called (read docs on generics and views - parsing, validating)
    def perform_create(self, serializer):
        url = serializer.validated_data['remote_url']
        photo = utils.photo_from_url(url)
        serializer.save(width=photo.width, height=photo.height, color=photo.color, image=photo.image)


class PhotoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    # TODO: make validations inside serializer, but also here for the url to the image, before serializer and its
    #  validator is called (read docs on generics and views - parsing, validating)
    def perform_update(self, serializer):
        # If the remote_url is updated, we need to update the image
        if serializer.validated_data.get('remote_url'):
            url = serializer.validated_data['remote_url']
            photo = utils.photo_from_url(url)
            serializer.save(width=photo.width, height=photo.height, color=photo.color, image=photo.image)
        else:
            serializer.save()

class PhotosUploadCreate(generics.CreateAPIView):
    serializer_class = PhotosUploadSerializer
