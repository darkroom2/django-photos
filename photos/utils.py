import re
import urllib.parse
from io import BytesIO

import requests
from django.core.files.uploadedfile import UploadedFile

from .models import Photo


def photo_from_url(url):
    width, height, color, ext = parse_url_path(url)

    if not ext:
        ext = '.png'

    # Check content-type
    response = requests.get(f'{url}{ext}')
    content_type = response.headers.get('Content-Type')
    if not content_type == f'image/{ext[1:]}':
        raise ValueError(f'Invalid file format: {content_type} or extension: {ext}')

    image_data = BytesIO(response.content)
    file_name = f'{width}x{height}_{color.replace("#", "")}{ext}'
    image = UploadedFile(image_data, file_name)

    return Photo(width=width, height=height, color=color, image=image)


def validate_photo_url(url):
    valid_url = validate_url(url)

    try:
        parse_url_path(valid_url)
    except IndexError as e:
        raise ValueError(f'Invalid URL: {url}') from e

    return url


def validate_url(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.scheme not in ('http', 'https') or not len(parsed_url.path) > 1:
            raise ValueError(f'Invalid URL: {url}')
    except ValueError:
        raise

    return url


def parse_url_path(url):
    match = re.findall(r'/(\d+)/([a-fA-F0-9]+)(.\w+$|$)', url)[0]
    width = height = int(match[0])
    color = f'#{match[1]:06}'
    ext = match[2]
    return width, height, color, ext
