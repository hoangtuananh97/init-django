import math
import os
import posixpath
from uuid import uuid4

from django.core.exceptions import SuspiciousOperation
from django.utils.deconstruct import deconstructible
from django.utils.encoding import filepath_to_uri
from django.utils.timezone import now
from storages.backends.s3boto3 import S3Boto3Storage
from storages.base import BaseStorage
from storages.utils import (
    safe_join,
    setting, )


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    file_overwrite = False

    def verify_file(self, content, validate_type_file, max_size_file, keep_name_file) -> tuple:
        file_size = content.size
        try:
            file_type = content.content_type.split('/')[1]
            file_type = file_type.lower()
        except Exception as e:
            raise ValueError('Error Format File. You need input file format {}'.format(','.join(validate_type_file)))

        if file_type not in validate_type_file:
            raise ValueError('File only {}'.format(','.join(validate_type_file)))
        if file_size > max_size_file:
            raise ValueError('Error Max length File is {} while file upload is {}'.format(convert_size(max_size_file),
                                                                                          convert_size(file_size)))
        file_name = str(uuid4()) + '.{}'.format(file_type)
        if keep_name_file:
            file_name = content.name
        return file_name

    def path_file_save_s3(self, location, file_name) -> str:
        return os.path.join('{}/'.format(location), now().date().strftime("%Y/%m/%d"), file_name)

    def save_file_pdf(self, content, keep_name_file=False):
        location = "pdf"
        max_size_file = 4194304
        validate_type_file = ['pdf']

        file_name = self.verify_file(content, validate_type_file, max_size_file, keep_name_file)
        path_file = self.path_file_save_s3(location, file_name)
        return self.save(path_file, content)

    def save_file_image(self, content, keep_name_file=False):
        location = "media"
        max_size_file = 4194304
        validate_type_file = ['png', 'jpg', 'jpeg']

        file_name = self.verify_file(content, validate_type_file, max_size_file, keep_name_file)
        path_file = self.path_file_save_s3(location, file_name)
        return self.save(path_file, content)

    def save_file_zip(self, content, keep_name_file=False):
        location = "zip"
        max_size_file = 4194304
        validate_type_file = ['zip']

        file_name = self.verify_file(content, validate_type_file, max_size_file, keep_name_file)
        path_file = self.path_file_save_s3(location, file_name)
        return self.save(path_file, content)


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


# model field char
def get_link(request, path_file):
    s3_boto3_storage = MediaRootS3Boto3Storage()
    custom_domain = setting('AWS_S3_CUSTOM_DOMAIN')
    if custom_domain:
        path_file = s3_boto3_storage._normalize_name(s3_boto3_storage._clean_name(path_file))
        if s3_boto3_storage.custom_domain:
            url = "{}//{}/{}".format(
                s3_boto3_storage.url_protocol, s3_boto3_storage.custom_domain, filepath_to_uri(path_file))
            return url
    else:
        request = request.context.get('request', None)
        if request is not None:
            return '{}://{}/{}'.format(request.scheme, request.get_host(), path_file)
    return path_file
