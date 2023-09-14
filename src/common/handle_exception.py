from http import HTTPStatus

from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException

from src.common.response import Responses


class ErrorMessages:
    default = "Unhandled Error"
    bad_request = "Bad request"
    un_authorized = "Unauthorized"
    wrong = "Something went wrong"
    not_found = "Not found"
    validation_error = "Validation error"


# custom APIException so it return the response by our general format, which is:
# {
#       "data": ...
#       "message": ...
#       "success": ...
# }
# We'll use this later in
# BadRequestException, NotFoundException, ValidationException, InternalException
# class below
class APIException(Exception):
    """
    Base class for all handled exception on API
    ...
    Attributes
    ----------
    http_status: HTTPStatus
        one of HTTPStatus which will be
    message: str
        brief message described the error
        can use `APICode.description` as default message
    extra: dict
        extra information related to the error
    """

    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    message = ErrorMessages.default
    data = None
    extra = None
    success = False

    def __init__(
        self,
        success=False,
        data=None,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        message=ErrorMessages.default,
        extra=None,
    ):
        """
        Parameters
        ----------
        :param code: APICode
            one of APICode which summarize result of operation
        :param http_status: HTTPStatus
            one of HTTPStatus which will be
        :param message: str
            brief message described the error
            can use `APICode.description` as default message
        :param extra: dict
            extra information related to the error
        """
        super().__init__()
        self.success = success
        self.data = data
        self.http_status = http_status
        self.message = message
        self.extra = extra

    # this function will automatically call in
    # BadRequestException, NotFoundException, ValidationException, InternalException
    # class below
    # so it will return the response by our general format, which is:
    # {
    #       "data": ...
    #       "message": ...
    #       "success": ...
    # }
    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
        }


# this function used @app.errorhandler() to trigger whenever an unexpected error show up
# normally, it will throw the error by default format of flask
# but with this @app.errorhandler(), it will catch and return the response as we want
# in other hand, it will allow us to custom the error response
def handle_exception(app: Flask):
    @app.errorhandler(APIException)
    def handle_api_exception(e: APIException):
        return jsonify(e.to_dict()), e.http_status

    @app.errorhandler(ValidationError)
    def handle_validation_exception(e: ValidationError):
        return Responses.not_ok_response(e.messages), HTTPStatus.BAD_REQUEST

    @app.errorhandler(HTTPException)
    def handle_http_error_exception(e):
        return Responses.not_ok_response(e.description), e.code

    @app.errorhandler(Exception)
    def handle_other_exceptions(e: Exception):
        return (
            Responses.not_ok_response("Internal Server Error: " + str(e)),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


# set default message and format for bad request exception
# we can transfer our custom "message" to this class,
# or else, it will show the default message
class BadRequestException(APIException):
    message = ErrorMessages.bad_request
    http_status = HTTPStatus.BAD_REQUEST

    def __init__(self, message=ErrorMessages.bad_request, extra=None):
        super().__init__(
            http_status=HTTPStatus.BAD_REQUEST, message=message, extra=extra
        )

    def __str__(self):
        return "Bad Request errors"


# set default message and format for not found exception
# we can transfer our custom "message" to this class,
# or else, it will show the default message
class NotFoundException(APIException):
    message = ErrorMessages.not_found
    http_status = HTTPStatus.NOT_FOUND

    def __init__(self, message=ErrorMessages.not_found, extra=None):
        super().__init__(http_status=HTTPStatus.NOT_FOUND, message=message, extra=extra)

    def __str__(self):
        return "Not Found errors"


# set default message and format for validation exception
# we can transfer our custom "message" to this class,
# or else, it will show the default message
class ValidationException(APIException):
    message = ErrorMessages.bad_request
    http_status = HTTPStatus.BAD_REQUEST

    def __init__(self, message=ErrorMessages.bad_request, extra=None):
        super().__init__(
            http_status=HTTPStatus.BAD_REQUEST, message=message, extra=extra
        )

    def __str__(self):
        return "Validation error"


# set default message and format for internal exception
# we can transfer our custom "message" to this class,
# or else, it will show the default message
class InternalException(APIException):
    message = ErrorMessages.default
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message=ErrorMessages.default, extra=None):
        super().__init__(
            http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
            message=message,
            extra=extra,
        )

    def __str__(self):
        return "Internal server error"
