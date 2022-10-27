import json
import re
import urllib.parse
from io import BytesIO
from pathlib import Path

import requests
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from .models import Photo


def photo_from_url(url):
    width, height, color = parse_url_path(url)

    ext = 'png'

    # Check content-type
    response = requests.get(f'{url}.{ext}')
    content_type = response.headers['Content-Type']
    if not content_type == f'image/{ext}':
        raise ValueError(f'Invalid file format: {content_type}, provide image/{ext}')

    image_data = BytesIO(response.content)
    file_name = f'{width}x{height}_{color}.{ext}'
    image = UploadedFile(image_data, file_name)

    return Photo(width=width, height=height, color=f'#{color}', image=image)


def validate_url(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme not in ('http', 'https') or not len(parsed_url.path) > 1:
            raise ValueError(f'Invalid URL: {url}')
    except ValueError:
        raise

    try:
        parse_url_path(url)
    except IndexError as e:
        raise ValueError(f'Invalid URL: {url}') from e

    return url


def parse_url_path(url):
    match = re.findall(r'/(\d+)/([a-fA-F0-9]+$)', url)[0]
    width = height = int(match[0])
    color = f'{match[1]:06}'
    return width, height, color


def get_json(json_url):
    try:
        validated_url = validate_url(json_url)
    except ValueError as val_err:
        try:
            json_file = Path(json_url).read_bytes()
        except (FileNotFoundError, IsADirectoryError) as file_err:
            raise file_err from val_err
        try:
            return json.loads(json_file)
        except json.JSONDecodeError:
            raise
    try:
        return requests.get(validated_url).json()
    except json.JSONDecodeError:
        raise


def photo_from_json(photo_data):
    _id = photo_data[settings.EXTERNAL_API_PHOTO_KEYS['id']]
    title = photo_data[settings.EXTERNAL_API_PHOTO_KEYS['title']]
    album_id = photo_data[settings.EXTERNAL_API_PHOTO_KEYS['album_id']]
    remote_url = photo_data[settings.EXTERNAL_API_PHOTO_KEYS['url']]

    photo = photo_from_url(remote_url)
    photo.id = _id
    photo.title = title
    photo.album_id = album_id

    return photo
