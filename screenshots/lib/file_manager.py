from django.conf import settings
import boto3


class FileManager:
    client = None
    bucket_name = settings.AWS_S3_BUCKET_NAME

    def __init__(self):
        self.client = self.__boto3_client()
        self.cloudfront_url = settings.CLOUDFRONT_DOMAIN

    def upload_to_s3_and_retrieve_url(self, file, filename, directory):
        filepath = f"{directory}/{filename}"

        self.upload_to_s3(file, filepath)
        return self.get_s3_object_for_file(filepath)

    def upload_to_s3(self, file, filepath):
        file.seek(0)
        self.client.upload_fileobj(file, self.bucket_name, filepath)

    def get_s3_object_for_file(self, filepath):
        return f'{self.cloudfront_url}/{filepath}'

    def delete_file_from_s3(self, filepath):
        self.client.delete_object(self.bucket_name, filepath)

    def __boto3_client(self):
        if self.client:
            return self.client

        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        return self.client
