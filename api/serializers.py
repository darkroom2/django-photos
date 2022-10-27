import json

import requests
from django.conf import settings
from rest_framework import serializers

from photos import utils
from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'title', 'album_id', 'width', 'height', 'color', 'url', 'remote_url')
        read_only_fields = ('id', 'width', 'height', 'color')
        extra_kwargs = {
            'title': {'required': False},
            'album_id': {'required': False},
            'remote_url': {'write_only': True, 'required': False},
            'url': {'read_only': True, 'source': 'image'}
        }


class PhotosUploadSerializer(serializers.Serializer):
    json_file = serializers.FileField(required=False)
    json_url = serializers.URLField(required=False)

    def create(self, validated_data):
        json_data = None

        # If json_file is provided, it should be a valid JSON
        if validated_data.get('json_file'):
            json_data = json.loads(validated_data['json_file'].read().decode('utf-8'))

        # If json_url is provided, it should be a valid JSON
        if validated_data.get('json_url'):
            json_data = json.loads(requests.get(validated_data['json_url']).content.decode('utf-8'))

        # Create photos from json
        photos_list = []
        for photo_data in json_data:
            photo = utils.photo_from_json(photo_data)
            photos_list.append(photo)

        # TODO: try using PhotoSerializer with param many=True???
        # bulk_create photos
        objs = Photo.objects.bulk_create(photos_list)
        return objs

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        # Only one field should be provided
        if data.get('json_file') and data.get('json_url'):
            raise serializers.ValidationError('Only one of fields (json_file, json_url) should be provided')

        # At least one field should be provided
        if not data.get('json_file') and not data.get('json_url'):
            raise serializers.ValidationError('At least one of fields (json_file, json_url) should be provided')

        json_data = None

        # If json_file is provided, it should be a valid JSON
        if data.get('json_file'):
            try:
                json_data = json.loads(data['json_file'].read().decode('utf-8'))
            except json.JSONDecodeError:
                raise serializers.ValidationError('Invalid file content, provide valid JSON')

        # If json_url is provided, it should be a valid JSON
        if data.get('json_url'):
            try:
                json_data = json.loads(requests.get(data['json_url']).content.decode('utf-8'))
            except json.JSONDecodeError:
                raise serializers.ValidationError('Invalid file content, provide valid JSON')

        # If json is valid, it should contain a list of photos
        if not isinstance(json_data, list):
            raise serializers.ValidationError('JSON should contain a list of photos')

        # Each photo should have proper photo keys
        # TODO: try validate using PhotoSerializer???
        for photo_data in json_data:
            for key in settings.EXTERNAL_API_PHOTO_KEYS.values():
                if key not in photo_data:
                    raise serializers.ValidationError(f'Photo {photo_data}, should have {key} field')
        return data
