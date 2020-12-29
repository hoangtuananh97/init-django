from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False

def return_image_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/shop-<id>/<return-order-id>/<filename>
    return f'{filename}'
