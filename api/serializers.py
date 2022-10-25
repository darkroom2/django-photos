from rest_framework import serializers

from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    width = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    dominant_color_hex = serializers.ReadOnlyField()

    class Meta:
        model = Photo
        fields = ('id', 'title', 'album_ID', 'width', 'height', 'dominant_color_hex', 'url')
