from rest_framework import serializers

from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'title', 'album_ID', 'width', 'height', 'dominant_color_hex', 'url')
        read_only_fields = ('id', 'width', 'height', 'dominant_color_hex')
