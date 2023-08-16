import logging
from io import BytesIO


from screenshots.lib.file_manager import FileManager

logger = logging.getLogger(__name__)


class ImageHelper:
    @staticmethod
    def upload_image_to_storage(image, filename, directory):
        thumb_url = ImageHelper.__generate_and_upload_thumbnail_to_storage(
            image, filename, directory
        )
        file_url = ImageHelper.__generate_and_upload_image_to_storage(
            image, filename, directory
        )

        return file_url, thumb_url

    @staticmethod
    def __generate_and_upload_thumbnail_to_storage(thumb, filename, directory):
        max_size = (200, 200)
        thumb.thumbnail(size=max_size)
        file = BytesIO()
        thumb.save(file, thumb.format)

        directory = f"{directory}/thumbnails"
        filename = f"thumb_{filename}"
        return ImageHelper.__upload(file, filename, directory)

    @staticmethod
    def __generate_and_upload_image_to_storage(image, filename, directory):
        file = BytesIO()
        image.save(file, image.format)
        return ImageHelper.__upload(file, filename, directory)

    @staticmethod
    def __upload(file, filename, directory):
        fm = FileManager()
        url = fm.upload_to_s3_and_retrieve_url(file, filename, directory)
        return url
