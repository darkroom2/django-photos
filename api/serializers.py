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

    def create(self, validated_data):
        remote_url = validated_data.get('remote_url')
        photo = utils.photo_from_url(remote_url)
        photo.title = validated_data.get('title')
        photo.album_id = validated_data.get('album_id')
        photo.remote_url = remote_url
        photo.save()
        return photo

    def update(self, instance, validated_data):
        # If the remote_url is updated, we need to update the image
        remote_url = validated_data.get('remote_url')
        if remote_url:
            photo = utils.photo_from_url(remote_url)
            instance.image = photo.image
            instance.width = photo.width
            instance.height = photo.height
            instance.color = photo.color
            instance.remote_url = remote_url
        instance.title = validated_data.get('title', instance.title)
        instance.album_id = validated_data.get('album_id', instance.album_id)
        instance.save()
        return instance

    def validate(self, attrs):  # TODO: figure out hell with required=True for create and required=False for update
        # Check if url is valid
        url = attrs.get('remote_url')
        try:
            utils.validate_url(url)
        except ValueError as e:
            raise serializers.ValidationError(e)

        # Generic validate the rest
        return super().validate(attrs)


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

        # External api photo fields are mapped is defined in settings
        converted_photos = []
        for photo_json in json_data:
            photo_converted = {settings.EXTERNAL_API_TO_PHOTO_FIELDS.get(key): value for key, value in
                               photo_json.items() if key in settings.EXTERNAL_API_TO_PHOTO_FIELDS}
            converted_photos.append(photo_converted)

        serializer = PhotoSerializer(data=converted_photos, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

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

        # Each element of the list should be a dict
        for photo_json in json_data:
            if not isinstance(photo_json, dict):
                raise serializers.ValidationError('Each element of the list should be a JSON')

        return data
