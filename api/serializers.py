from rest_framework import serializers

from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(read_only=True, source='image')
    remote_url = serializers.URLField(write_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'title', 'album_id', 'width', 'height', 'color', 'url', 'remote_url')
        read_only_fields = ('id', 'width', 'height', 'color')
