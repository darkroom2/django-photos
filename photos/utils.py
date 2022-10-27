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


def photo_from_url(url):
    match = re.findall(r'/(\d+)/([a-fA-F0-9]+)', url)[0]
    width = height = int(match[0])
    color = f'{match[1]:06}'

    ext = '.png'

    image_data = requests.get(f'{url}{ext}').content
    file_name = f'{width}x{height}_{color}{ext}'

    image = UploadedFile(BytesIO(image_data), file_name)

    return Photo(width=width, height=height, color=f'#{color}', image=image, remote_url=url)


# TODO: verify usages and remove probably or use it in Serializer
def validate_url(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme not in ('http', 'https') or not len(parsed_url.path) > 1:
            raise ValueError(f'Invalid URL: {url}')
    except ValueError:
        raise
    return url


# TODO: verify usages and remove probably or use it in Serializer (method too complex to be util, does validation and
#  then stuff, split this)
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
