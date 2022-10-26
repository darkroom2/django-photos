import json
import logging
import re
import urllib.parse
from io import BytesIO
from pathlib import Path

import requests
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from .models import Photo

logger = logging.getLogger(__name__)


def parse_url(url):
    validated_url = validate_url(url)

    width = 0
    height = 0
    color = 'ffffff'

    match = re.findall(r'/(\d+)/([a-fA-F0-9]+)', url)
    if match:
        result = match[0]
        width = height = int(result[0])
        color = f'{result[1]:06}'

    ext = Path(validated_url).suffix
    if not ext:
        ext = '.png'
        url = f'{url}{ext}'

    image_data = requests.get(url).content

    if not match:
        width = 0  # TODO: get width from downloaded image
        height = 0  # TODO: get height from downloaded image
        color = 'ffffff'  # TODO: get color from downloaded image

    file_name = f'{width}x{height}_{color}{ext}'
    image = UploadedFile(BytesIO(image_data), file_name)
    return Photo(width=width, height=height, color=f'#{color}', image=image)


def validate_url(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme not in ('http', 'https') or not len(parsed_url.path) > 1:
            raise ValueError(f'Invalid URL: {url}')
    except ValueError:
        raise
    return url


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


def prepare_photo(photo_data):
    try:
        _id = photo_data[settings.EXTERNAL_API_PHOTO_KEYS['id']]
        title = photo_data[settings.EXTERNAL_API_PHOTO_KEYS['title']]
        album_id = photo_data[settings.EXTERNAL_API_PHOTO_KEYS['album_id']]
        photo_url = photo_data[settings.EXTERNAL_API_PHOTO_KEYS['url']]
    except KeyError as e:
        logger.error(f'Invalid JSON format: {photo_data}, missing: {e}')
        return None

    if Photo.objects.filter(pk=_id).exists():
        logger.warning(f'The photo from {photo_data} already exists')
        return None

    photo = parse_url(photo_url)
    photo.id = _id
    photo.title = title
    photo.album_id = album_id
    return photo
