import base64
import uuid
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.db import models
from django.conf import settings


class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == settings.DATABASE_ENGINE:
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)


class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == settings.DATABASE_ENGINE:
            return "tinyint unsigned"
        else:
            return super(PositiveTinyIntegerField, self).db_type(connection)


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.
    """

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, str):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')
                if header.split("/")[0] not in settings.ALLOW_FILE_TYPES:
                    raise Exception("Invalid File")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    @staticmethod
    def get_file_extension(file_name, decoded_file):
        image = Image.open(BytesIO(decoded_file))
        extension = image.format.lower()
        extension = "jpg" if extension == "jpeg" else extension
        return extension
