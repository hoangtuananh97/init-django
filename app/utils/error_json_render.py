from _datetime import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if isinstance(exc, PageNotFound):
        response.data = None
        return response

    if response is not None:
        code = exc.default_code
        message = exc.detail
        response.data = {
            'status': "ERROR",
            'body': None,
            'error': {
                'message': message,
                'code': code,
                'timestamp': datetime.now(),
            }
        }
        response.content_type = 'application/json'

    return response


class PageNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found.'
    default_code = 'not_found'


class BadRequestException(APIException):
    status_code = 400
    default_detail = 'Bad request'
    default_code = 'bad_request'


class EmailNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Email not found'
    default_code = 'email_not_found'


class IdInvalid(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Id not found'
    default_code = 'id_not_found'


class TokenInvalid(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Token not found'
    default_code = 'token_not_found'


class UserIsActivated(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User is activate'
    default_code = 'user_is_activated'


class NotMatchPassword(APIException):
    default_detail = 'Not match password'
    default_code = 'not_match_password'


class IntegrityDataError(APIException):
    default_detail = 'Integrity data error'
    default_code = 'integrity_data_error'


class ServerDatabaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Server Database Error'
    default_code = 'server_database_error'


class LoginInvalid(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'User unauthorized'
    default_code = 'user_unauthorized'


class UserNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'User not found'
    default_code = 'user_not_found'


class UserIsActivatedOrIsDeleted(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User is not activate or deleted'
    default_code = 'user_is_activated_or_deleted'

class ErrorFormatFile(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error Format File'
    default_code = 'error_format_file'


class ErrorMaxLengthFile(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error Max length File'
    default_code = 'error_length_file'
