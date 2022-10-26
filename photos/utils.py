import logging
import re
import urllib.parse
from io import BytesIO
from pathlib import Path

from django.core.files.uploadedfile import UploadedFile
from requests import get

from .models import Photo

logger = logging.getLogger(__name__)


def parse_url(url):
    validated_url = validate_url(url)

    width = 0
    height = 0
    color = 'ffffff'

    match = re.findall(r'/(\d+)/([a-fA-F0-9]+)', url)  # hex atleast 4 digits in case last two are 00 and cut off
    if match:
        result = match[0]
        width = height = int(result[0])
        color = f'{result[1]:06}'

    ext = Path(validated_url).suffix
    if not ext:
        ext = '.png'
        url = f'{url}{ext}'

    image_data = get(url).content

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
    except ValueError as e:
        logger.error(e)
        raise
    return url
