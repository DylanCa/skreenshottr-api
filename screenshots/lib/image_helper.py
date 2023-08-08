import logging

from screenshots.lib.file_manager import FileManager

logger = logging.getLogger(__name__)


class ImageHelper:

    @staticmethod
    def upload_to_storage(file, directory):
        fm = FileManager()
        url = fm.upload_to_s3_and_retrieve_url(file, directory)

        return url
