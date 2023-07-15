import logging
import urllib.request
from typing import TextIO

from PIL import Image
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


class ImageHelper:

    @staticmethod
    def verify_image_from_file(file) -> bool:
        try:
            img = Image.open(file)
            img.verify()
            return True
        except Exception as e:
            logger.exception(e)
            return False

    @staticmethod
    def save_image_in_storage(file: TextIO) -> str:
        file_name = default_storage.save(file.name, file)
        return default_storage.url(file_name)
