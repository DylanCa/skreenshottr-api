import logging

from PIL import Image
from screenshots.lib.file_manager import FileManager

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
    def save_image_in_storage(file, directory):
        fm = FileManager()
        url = fm.upload_to_s3_and_retrieve_url(file, directory)

        return url
