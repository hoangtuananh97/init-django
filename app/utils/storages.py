import posixpath
from datetime import timedelta, datetime

from django.core.exceptions import SuspiciousOperation
from django.utils.deconstruct import deconstructible
from django.utils.encoding import filepath_to_uri
from storages.backends.s3boto3 import S3Boto3Storage
from storages.base import BaseStorage
from storages.utils import (
    check_location, get_available_overwrite_name, lookup_env, safe_join,
    setting, to_bytes,
)


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


# return path image
def return_image_upload_path(instance, filename):
    return f'images/{filename}'


@deconstructible
class S3Boto3StorageABC(BaseStorage):
    location = ''
    custom_domain = setting('AWS_S3_CUSTOM_DOMAIN')
    url_protocol = 'https:'
    querystring_expire = 3600

    def _clean_name(self, name):
        """
        Cleans the name so that Windows style paths work
        """
        # Normalize Windows style paths
        clean_name = posixpath.normpath(name).replace('\\', '/')

        # os.path.normpath() can strip trailing slashes so we implement
        # a workaround here.
        if name.endswith('/') and not clean_name.endswith('/'):
            # Add a trailing slash as it was stripped.
            clean_name += '/'
        return clean_name

    def _normalize_name(self, name):
        """
        Normalizes the name so that paths like /path/to/ignored/../something.txt
        work. We check to make sure that the path pointed to is not outside
        the directory specified by the LOCATION setting.
        """
        try:
            return safe_join(self.location, name)
        except ValueError:
            raise SuspiciousOperation("Attempted access to '%s' denied." %
                                      name)

    def url(self, name, parameters=None, expire=None, http_method=None):
        # Preserve the trailing slash after normalizing the path.
        name = self._normalize_name(self._clean_name(name))
        # if expire is None:
        #     expire = self.querystring_expire

        if self.custom_domain:
            url = "{}//{}/{}".format(
                self.url_protocol, self.custom_domain, filepath_to_uri(name))
            return url
